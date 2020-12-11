from flask import Flask
from flask import request
from flask_mqtt import Mqtt
from credential import *
from tools import *
import json


app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = MQTT_BROKER
app.config['MQTT_BROKER_PORT'] = MQTT_PORT
app.config['MQTT_USERNAME'] = MQTT_USER
app.config['MQTT_PASSWORD'] = MQTT_PASS
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)


@app.route('/')
def test_api():
    print("hello")
    return API_RESPONSE_TEST


@app.route('/api/manvalve', methods=['POST'])
def manvalve():
    # json_data = request.json # just if you received a perfect string data, for other you will need:
    json_data = request.data
    # print_s(json_data)
    json_data = json.loads(json_data)
    send_ok_response = True
    uuid = json_data['uuid']
    for valve in json_data['valves']:
        time = str(valve['time'])
        valve_pass = int(valve['v']) <= 128
        action_pass = int(valve['action']) == 0 or int(valve['action']) == 1
        time_pass = len(time) == 5 and int(time[0]) <= 1
        if (valve_pass and action_pass and time_pass):
            pass
        else:
            send_ok_response = False
    if (send_ok_response):
        json_data["id"] = 1
        json_data.pop('uuid')
        msg = json.dumps(json_data)
        mqtt.publish(uuid+'/manvalve/app', msg, 0, False)
        return REQUEST_RESPONSE['OK'], 200
    else:
        return REQUEST_RESPONSE['JSON_ERROR'], 406


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
            json_data = request.json
            json_datason_data = request.json
            uuid = str(json_data['uuid'])
            prog = str(json_data['prog']).upper()
            water = int(json_data['water'])
            if prog in "ABCDEF" and water > 0 and water <= 400 and len(uuid) < 40:
                msg = "{\"id\":1,\"prog\":\"" + \
                    str(prog) + "\",\"water\":" + str(water) + "}"
                mqtt.publish(uuid+'/program/app',
                             msg, 0, False)
                return REQUEST_RESPONSE['OK'], 200
            else:
                return REQUEST_RESPONSE['NOP']
        except:
            return REQUEST_RESPONSE['PUBLISH_ERROR']


if __name__ == '__main__':
    app.run()
