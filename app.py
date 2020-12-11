from flask import Flask
from flask import request
from flask_mqtt import Mqtt
from credential import *

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = MQTT_BROKER
app.config['MQTT_BROKER_PORT'] = MQTT_PORT
app.config['MQTT_USERNAME'] = MQTT_USER
app.config['MQTT_PASSWORD'] = MQTT_PASS
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)

@app.route('/')
def test_api():
    return API_RESPONSE_TEST

@app.route('/api/manvalve')
def manvalve():
    return API_RESPONSE_TEST

@app.route('/api/manprog')
def manprog():
    return API_RESPONSE_TEST

@app.route('/api/general')
def general():
    return API_RESPONSE_TEST

@app.route('/api/stop')
def stop():
    return API_RESPONSE_TEST

@app.route('/api/program', methods=['POST'])
def program():
    if request.method == 'POST':
        try:
            json_data = request.json
            uuid = str(json_data['uuid'])
            prog = str(json_data['prog']).upper()
            water = int(json_data['water'])
            if prog in "ABCDEF" and water > 0 and water <= 400 and len(uuid) < 40:
                msg = "{\"id\":1,\"prog\":\"" + \
                    str(prog) + "\",\"water\":" + str(water) + "}"
                mqtt.publish(uuid+'/program/app',
                            msg, 0, False)
                return  REQUEST_RESPONSE['PUBLISH_ERROR'], 200
            else:
                return REQUEST_RESPONSE['NOP']
        except:
                return REQUEST_RESPONSE['NOP']

if __name__ == '__main__':
    app.run()
