# Import Libraries
from flask import Flask, render_template, Response, redirect, url_for, request, jsonify, send_file, flash, session
from flask import request, make_response
from flask_bcrypt import Bcrypt
from forms import LoginForm
from models import db, Users
from mqdtect import mqttObserver
from threadcv import *
from functools import wraps
import socket, struct
import psycopg2, uuid, json, yaml, itertools
import pandas as pd
import numpy as np
import logging, random, time
import paho.mqtt.client as mqtt

from ultralytics import YOLO
import supervision as sv


#Load models
MODEL = 'models/best.pt'

# Instantiate connection to PostgresDB
with open ("secret.yml", 'r') as f:
    data = yaml.full_load(f)

param_dic = {
    "host"      : data.get('host'),
    "database"  : data.get('database'),
    "user"      : data.get('user'),
    "password"  : data.get('password')
}

app = Flask(__name__)

# connect to flespi.io using paho mqtt python
# Define the MQTT broker parameters
BROKER = 'mqtt.flespi.io'
PORT = 1883  # Default MQTT port, you can use 8883 for SSL/TLS
TOPIC = 'yolo'

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{data.get('user')}:{data.get('password')}@{data.get('host')}/{data.get('database')}'
bcrypt = Bcrypt()

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usr_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print("Connection successful")
    return conn
    
def fetch_tables():
    conn = connect(param_dic)
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return tables

def fetch_data(sql_query):
    conn = connect(param_dic)
    cur = conn.cursor()
    cur.execute(sql_query)
    results = cur.fetchall()
    columns = [desc[0] for desc in cur.description]  # Get column names
    cur.close()
    conn.close()
    return results, columns

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response
    
# Generate random temperature
def get_temp_reading():
    return random.randint(20, 50)

def find_camera(id):
    cameras = ['test_video/test2.mp4']
    return cameras[int(id)]
    #  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
    #  for webcam use zero(0)

# Global video source variable
video_source = None

# Handle threading process    
def stop_stream():
    global video_source
    if video_source is not None:
        video_source.stop()
        video_source = None

# Process frame
def get_frames(camera_id):
    global video_source
    #initialize the YOLOv8 model here
    model = YOLO(MODEL)
    model.fuse()
    obs = mqttObserver(BROKER, PORT, TOPIC)
    obs2 = mqttObserver(BROKER, PORT, 'temperature')
    tracker = sv.ByteTrack() #track_activation_threshold=0.8
    corner_annotator = sv.BoxCornerAnnotator(thickness=2)
    label_annotator = sv.LabelAnnotator()
    detection_list = []
    cam = find_camera(camera_id)
    video_source = SpeedmeUp(cam).start()
    # Time intervals
    last_message = 0
    message_interval = 5
    while True:
        start_time = time.time()
        frame = video_source.read()
        if frame is None:
            break
            
        result = model(frame, conf=0.7)[0]
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        detections = sv.Detections.from_ultralytics(result)
        detections = tracker.update_with_detections(detections)
        payload = {tracker_id: result.names[class_id] for class_id, tracker_id in zip(detections.class_id, detections.tracker_id)}
        detection_list.append(detections.tracker_id)

        # Publish random temperature
        if (time.time() - last_message) > message_interval:
            random_temp = get_temp_reading()
            obs2.mqtt_pub_randtemp(random_temp)
            last_message = time.time()
            
        # Flatten the detection_list using itertools.chain
        flat_list = list(itertools.chain(*detection_list))

        for element in flat_list:
            obs.mqtt_watch(element, 'CAMERA-1', payload, timestamp) #publish detection
        
        # if not ret:
        #     break

        frame = corner_annotator.annotate(scene=frame.copy(), detections=detections)
        frame = label_annotator.annotate(scene=frame, detections=detections)

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')   
        elapsed_time = time.time() - start_time
        logging.debug(f"Frame generation time: {elapsed_time} seconds")
    
# Route to render the HTML template-
@app.route('/')
def index():
     #return render_template('videoFeed.html')
     # return redirect(url_for('video_feed')) #to render live stream directly
    return redirect(url_for('login'))

@app.route("/login", methods=['GET','POST'])
def login():
    if 'usr_id' in session:
        return redirect(url_for('panel'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['usr_id'] = user.id
            session['username'] = user.username
            flash('You have been Logged in!', 'success')
            return redirect(url_for('panel'))
            
        else:
            flash('INVALID PASSWORD', 'danger')
            
    return render_template('login.html', form=form)

# Route to render the HTML template
@app.route("/part1", methods=['GET','POST'])
@login_required
def panel():
    return render_template('partI.html')

# Route to render the HTML template
@app.route("/part2", methods=['GET','POST'])
@login_required
def panel2():
    tables = fetch_tables()  # Get table names for the dropdown
    stop_stream() # Stop the video stream on redirection to other page
    return render_template('partII.html', tables=tables)


# Postgre endpoint
@app.route('/execute_query', methods=['POST'])
def execute_query():
    sql_query = request.json.get('query')
    try:
        results, columns = fetch_data(sql_query)
        return jsonify({'results': results, 'columns': columns})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/fetch_table', methods=['POST'])
def fetch_table():
    table_name = request.json.get('table_name')
    try:
        results, columns = fetch_data(f"SELECT * FROM {table_name}")
        return jsonify({'results': results, 'columns': columns})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/query1', methods=['POST'])
def query1():
    sql_query = """SELECT UPPER(first_name) as upper_first_name FROM students"""  # Query1
    try:
        results, columns = fetch_data(sql_query)
        return jsonify({'output_query':sql_query, 'results': results, 'columns': columns})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/query2', methods=['POST'])
def query2():
    sql_query = """SELECT DISTINCT major FROM students"""  # Query2
    try:
        results, columns = fetch_data(sql_query)
        return jsonify({'output_query':sql_query, 'results': results, 'columns': columns})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/query3', methods=['POST'])
def query3():
    sql_query ="""SELECT s.*, sch.scholarship_amount AS scholarship_amount FROM students s LEFT JOIN scholarships sch ON s.student_id = sch.student_ref_id;"""  # Query3
    try:
        results, columns = fetch_data(sql_query)
        return jsonify({'output_query':sql_query, 'results': results, 'columns': columns})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/query4', methods=['POST'])
def query4():
    sql_query = """SELECT s.student_id, first_name, last_name FROM students s LEFT JOIN scholarships sch ON s.student_id = sch.student_ref_id WHERE sch.student_ref_id IS NULL;""" # Query4
    try:
        results, columns = fetch_data(sql_query)
        return jsonify({'output_query':sql_query, 'results': results, 'columns': columns})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route("/logout")
@login_required
def logout():
    session.pop('usr_id')
    session.pop('username')
    stop_stream() # Stop the video stream on logout
    
    flash("You have been Logout", "success")
    return redirect(url_for('login'))

@app.route('/video_feed/<string:id>/', methods=["GET"])
def video_feed(id):
    return Response(get_frames(id),mimetype='multipart/x-mixed-replace; boundary=frame')
    
if __name__ == "__main__":
    app.run(host='192.168.1.19', port=4455, threaded=True, debug=True)
    # socketio.run(app, host='192.168.1.19', port=4455, use_reloader=False, debug=False)