Object Detection Flask App (Exam)
==============================

For the given task, I decided to choose the real-time object detection machine learning
model from YOLOv8 (You Only Look Once) and integrate it with Flask application.

#NOTE:
I was not able to deploy it in the cloud due to memory space issue I was not able to anticipate it early on.
However, I recorded a video to demonstrate the functionality of the app and to show that its working.
My apology for not able to comply with the instruction given in PART I.


## Links

Kindly check the following links for more information on YOLOv8 and Flask:

- YOLO Community page: <https://docs.ultralytics.com/>
- Flask: <https://flask.palletsprojects.com/en/3.0.x/>

## Features

- Real-time object detection using YOLO.
- **Real-time data transmission via MQTT**: Send detected object data to
MQTT brokers (Flespi.io) for real-time monitoring and integration with IoT systems.
- Simple web interface for interacting dynamic tables. (PART II Exam)

## Training Process

Kindly check <https://colab.research.google.com/drive/1JsEVYdxxMgB5w1j8SMyRHb1NOiQOuLhM?usp=sharing> for details
on how the training process works. Below for the resource 
<https://drive.google.com/drive/folders/1CTY3Kr_RggHAFwM702a-URzCeK-jiC3e?usp=sharing>


## Documentation

Documentation for the Flespi.io broker, clients and connections can be found in
the main page, which are available online at <https://flespi.com/>. There
are also pages with an introduction to the features of MQTT.

## DATABASE (Part II)

Query used:
	1. """SELECT UPPER(first_name) as upper_first_name FROM students"""
	2. """SELECT DISTINCT major FROM students"""
	3. """SELECT s.*, sch.scholarship_amount AS scholarship_amount FROM students s LEFT JOIN scholarships sch ON s.student_id = sch.student_ref_id;""
	4. """SELECT s.student_id, first_name, last_name FROM students s LEFT JOIN scholarships sch ON s.student_id = sch.student_ref_id WHERE sch.student_ref_id IS NULL;"""
