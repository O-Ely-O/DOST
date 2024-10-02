import paho.mqtt.client as mqtt
import yaml

# Instantiate connection to Flespi.io
with open ("secret.yml", 'r') as f:
    data = yaml.full_load(f)

class mqttObserver():
    def __init__(self, mqtt_broker, mqtt_port, mqtt_topic, initial_data=None):
        self._set = set(initial_data) if initial_data else set()
        self._previous_values = set()  # Track previously added values
        # Initialize flespi username and password for the connection
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic
        self.client = mqtt.Client()
        self.client.username_pw_set(data.get('token'), "")

        # Assign event callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
        
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        # Subscribe to a topic here if needed
        self.client.subscribe(self.mqtt_topic)

    def on_message(self, client, userdata, msg):
        print(f"Message received: {msg.payload.decode()}")

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print(f"Unexpected disconnection. Result code: {rc}")
        else:
            print("Disconnected successfully")
        
    def _publish_detection(self, value, client_id, payload, timestamp):
        if value in payload:
            msg = (f"{client_id}: {value}:{payload[value]}: {timestamp}")
            self.client.publish(self.mqtt_topic, msg)

    def mqtt_watch(self, value, client_id, payload, timestamp):
        if value in self._previous_values:
            # Do not add and do not print message if the value was added before
            return
        if value not in self._set:
            self._set.add(value)
            self._previous_values.add(value)  # Track the value as added
            self._publish_detection(value, client_id, payload, timestamp)

    def mqtt_pub_randtemp(self, value):
        msg = (f"{value}")
        self.client.publish(self.mqtt_topic, msg)

    def discard(self, value):
        if value in self._set:
            self._set.discard(value)
            self._previous_values.discard(value)  # Optionally, remove from previous_values as well
    
    def remove(self, value):
        if value in self._set:
            self._set.remove(value)
            self._previous_values.discard(value)  # Optionally, remove from previous_values as well
    
    def __contains__(self, value):
        return value in self._set
    
    def __iter__(self):
        return iter(self._set)
    
    def __repr__(self):
        return repr(self._set)