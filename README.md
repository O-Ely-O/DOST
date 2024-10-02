Object Detection Flask App (Exam)
==============================

For the given task, I decided to choose the real-time object detection machine learning
model from YOLOv8 (You Only Look Once) and Integrate it with Flask application.

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

## Deployment
The app was deployed in AWS (free tier) account together with the other services
	- Elastic Beanstalk (compute engine)
	- RDS (database)

## Quick start

Here are the guides/instruction on how to access the web

1. **Access the Login Page**: Navigate to `http://127.0.0.1:5000/login` in your web browser.
2. **Enter Credentials**: Use the following default credentials to log in:
	- **Username**: `admin@test.com`
	- **Password**: `admin`
3. **Click 'Login'**: After entering your credentials, click the 'Login' button to access the application.

## Documentation

Documentation for the Flespi.io broker, clients and connections can be found in
the main page, which are available online at <https://flespi.com/>. There
are also pages with an introduction to the features of MQTT.

