import traceback
import json

from flask import Flask, request, jsonify, render_template, redirect
from flask_socketio import SocketIO
from flask_socketio import send, emit

app = Flask(__name__)
app.secret_key = 'ptSecret'
app.config['SECRET_KEY'] = 'ptSecret'
socketio = SocketIO(app)

# ---- MQTT ----
import paho.mqtt.client as mqtt
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("MQTT Conectado")


def mqtt_connect():
    if client.is_connected() is False:
        try:
            client.connect("localhost", 1883, 10)
            print("Conectado al servidor MQTT")
            client.loop_start()
        except:
            print("No pudo conectarse")


# ---- Endpoints ----
@app.route('/')
def home():
    mqtt_connect()
    return render_template('index.html')


# ---- Web sockets contra el frontend ----
@socketio.on('camera_event')
def ws_camera_event(data):
    topic = json.loads(data)["topic"]
    client.publish(topic, data)


if __name__ == "__main__":
    client.on_connect = on_connect
    # IN LOCAL HOST Certificados SSL:
    # https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
    app.run(debug=True, host="0.0.0.0", port=5020, ssl_context='adhoc')

    # IN REMOTE HOST
    #app.run(debug=True, host="0.0.0.0", port=5020)
