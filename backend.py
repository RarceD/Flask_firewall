from flask import Flask, render_template, request
from flask_mqtt import Mqtt
from flask_cors import CORS
from credential import *
from dB.apikey import Apikey
from calculations.calculateEto import calculateEto
from calculations.cropstages import Cropstages
from dB.db_interactions import Db_handler
from databaseinteractions import DatabaseInteractions
from tools import *
import json
import time

# Inicialize the mqtt class and set the credentials for the correct connection:
app = Flask(__name__)
CORS(app)
app.config['MQTT_BROKER_URL'] = MQTT_BROKER
app.config['MQTT_BROKER_PORT'] = MQTT_PORT
app.config['MQTT_USERNAME'] = MQTT_USER
app.config['MQTT_PASSWORD'] = MQTT_PASS
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)

# In every post I check if they have a valid key to use them.
# Create a AssociationUuidClient data type and check  all the available uuid for each client
data_keys = Apikey()
data_keys.load_asssociation('data/uuid_client_real.json')

"""
All the diferent web pages:

"""
@app.route('/')
def init_https():
    return render_template('index.html')


@app.route('/guide')
def test_api():
    return render_template('guide.html')


@app.route('/testcors')
def test_api2():
    return "no problem with cors"


@app.route('/calculate')
def calculate_eto():
    return render_template('calculate.html')


"""

Mqtt listeners in case of watching the evolution of the controllers:

"""
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('abcab9a1-8b22-40b0-b4bf-fb8e182f7508/test')
    # mqtt.publish('abcab9a1-8b22-40b0-b4bf-fb8e182f7508/2',
    #              'mqtt server start!!')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    # mqtt.publish('abcab9a1-8b22-40b0-b4bf-fb8e182f7508/on_message', 'mqtt')
    # print_s(data)


"""

Diferent endpoint to POST and publish the information:

"""
@app.route('/api/cal_etc', methods=['GET', 'POST'])
def cal_etc():
    # If I received data I calculate it with them, if not make it with aemet
    if request.method == 'GET':
        if request.data:
            json_data = json.loads(request.data)
            et0 = calculateEto()
            if (et0.load_file(json_data)):
                return 'et0: '+str(et0.calc_eto())
            else:
                return REQUEST_RESPONSE['JSON_ERROR'], 406
        else:
            et0 = calculateEto()
            et0.get_data()
            return str(et0.calc_eto())
    elif request.method == 'POST':
        json_data = json.loads(request.data)
        # print_s(request.data)
        # print_s(json_data)
        et0 = calculateEto()
        if (et0.load_file(json_data)):
            return str(et0.calc_eto())
        else:
            return REQUEST_RESPONSE['JSON_ERROR'], 406
 
        # else:
        #     return REQUEST_RESPONSE['JSON_ERROR'], 406


@app.route('/api/manvalve', methods=['POST'])
def manvalve():
    # json_data = request.json # just if you received a perfect string data, for other you will need:
    json_data = request.data
    # print_s(json_data)
    json_data = json.loads(json_data)
    send_ok_response = True
    uuid = ""
    client = ""
    try:
        uuid = json_data['uuid']
        client = json_data['client']
    except:
        return REQUEST_RESPONSE['JSON_ERROR'], 406
    db = Db_handler("dB/db_production")
    if (db.check_uuid_is_association(uuid_received=uuid, client_received=client)):
        for valve in json_data['valves']:
            time = str(valve['time'])
            valve_pass = int(valve['v']) <= 128
            action_pass = int(valve['action']) == 0 or int(
                valve['action']) == 1
            time_pass = len(time) == 5 and int(time[0]) <= 1
            if (valve_pass and action_pass and time_pass):
                pass
            else:
                send_ok_response = False
        if (send_ok_response):
            json_data["id"] = 1
            json_data.pop('client')
            json_data.pop('uuid')
            msg = json.dumps(json_data)
            mqtt.publish(uuid+'/manvalve/app', msg, 0, False)
            return REQUEST_RESPONSE['OK'], 200
        else:
            return REQUEST_RESPONSE['JSON_ERROR'], 406
    else:
        return REQUEST_RESPONSE['CLIENT_ERROR'], 406


@app.route('/api/manprog', methods=['POST'])
def manprog():
    json_data = request.data
    json_data = json.loads(json_data)
    send_ok_response = False
    uuid = ""
    client = ""
    try:
        uuid = json_data['uuid']
        client = json_data['client']
    except:
        return REQUEST_RESPONSE['JSON_ERROR'], 406
    db = Db_handler("dB/db_production")
    if (db.check_uuid_is_association(uuid_received=uuid, client_received=client)):
        if json_data['prog'] in "ABCDEF" and int(json_data['action']) <= 1:
            send_ok_response = True
        if (send_ok_response):
            json_data["id"] = 1
            json_data.pop('uuid')
            json_data.pop('client')
            msg = json.dumps(json_data)
            mqtt.publish(uuid+'/manprog/app', msg, 0, False)
            return REQUEST_RESPONSE['OK'], 200
        else:
            return REQUEST_RESPONSE['JSON_ERROR'], 406
    else:
        return REQUEST_RESPONSE['CLIENT_ERROR'], 406


@app.route('/api/general', methods=['POST'])
def general():
    json_data = request.data
    json_data = json.loads(json_data)
    uuid = ""
    client = ""
    try:
        uuid = str(json_data['uuid'])
        client = json_data['client']
    except:
        return REQUEST_RESPONSE['PUBLISH_ERROR'], 407

    db = Db_handler("dB/db_production")
    if (db.check_uuid_is_association(uuid_received=uuid, client_received=client)):
        # implement a filter to check if msg is ok:
        send_ok_response = True
        if "pump_delay" in json_data:
            pump_delay = int(json_data["pump_delay"])
            if pump_delay < -120 or pump_delay > 120:
                send_ok_response = False
        if "valve_delay" in json_data:
            valve_delay = int(json_data["valve_delay"])
            if valve_delay < 0 or valve_delay > 120:
                send_ok_response = False
        if "pause" in json_data:
            pause = int(json_data["pause"])
            if (pause > 7 or pause < 0):
                send_ok_response = False
        if "fertirrigations" in json_data:
            fertirrigations = json_data["fertirrigations"]
            if (len(fertirrigations) != 32):
                send_ok_response = False
        if "fertirrigation_number" in json_data:
            fertirrigation_number = int(json_data["fertirrigation_number"])
            if (fertirrigation_number > 4):
                send_ok_response = False
        if "date" in json_data:
            date = json_data["date"]
            if (len(date) != 16):
                send_ok_response = False
        if "pump_ids" in json_data:
            pump_ids = json_data["pump_ids"]
            if (len(pump_ids) != 16):
                send_ok_response = False
        if "master_pump_associations" in json_data:
            master_pump_associations = json_data["master_pump_associations"]
            if (len(master_pump_associations) != 32):
                send_ok_response = False
        if "master_associations" in json_data:
            master_associations = json_data["master_associations"]
            if (len(master_associations) != 128):
                send_ok_response = False

        if send_ok_response:
            json_data["id"] = 1
            json_data.pop('client')
            json_data.pop('uuid')
            msg = json.dumps(json_data)
            mqtt.publish(uuid+'/general/app', msg, 0, False)
            return REQUEST_RESPONSE['OK'], 200
        else:
            return REQUEST_RESPONSE['JSON_ERROR'], 406
    else:
        return REQUEST_RESPONSE['CLIENT_ERROR'], 406


@app.route('/api/stop', methods=['POST'])
def stop():
    json_data = request.data
    json_data = json.loads(json_data)
    uuid = ""
    client = ""
    try:
        uuid = str(json_data['uuid'])
        client = json_data['client']
    except:
        return REQUEST_RESPONSE['PUBLISH_ERROR'], 407
    db = Db_handler("dB/db_production")
    if (db.check_uuid_is_association(uuid_received=uuid, client_received=client)):
        json_data["id"] = 1
        json_data.pop('uuid')
        json_data.pop('client')
        msg = json.dumps(json_data)
        mqtt.publish(uuid+'/stop/app', msg, 0, False)
        return REQUEST_RESPONSE['OK'], 200
    else:
        return REQUEST_RESPONSE['CLIENT_ERROR'], 406


@app.route('/api/program', methods=['POST'])
def program():
    # Parse the data:
    json_data = request.data
    json_data = json.loads(json_data)
    # Mandatory msg information:
    uuid = ""
    prog = ""
    client = ""
    try:
        uuid = str(json_data['uuid'])
        prog = str(json_data['prog']).upper()
        client = json_data['client']
    except:
        return REQUEST_RESPONSE['PUBLISH_ERROR'], 407
    db = Db_handler("dB/db_production")
    if (db.check_uuid_is_association(uuid_received=uuid, client_received=client)):

        # i check if the parameters are ok:
        send_ok_response = True
        if prog not in "ABCDEF":
            send_ok_response = False
        if "water" in json_data:
            water = int(json_data['water'])
            if water < 0 or water > 400:
                send_ok_response = False
        if "starts" in json_data:
            starts = json_data['starts']
            if len(starts) > 6:
                send_ok_response = False
            for s in starts:
                if len(s) < 5:
                    send_ok_response = False
        if "interval" in json_data:
            interval = int(json_data["interval"])
            if interval > 7:
                send_ok_response = False
        if "interval_init" in json_data:
            interval_init = int(json_data["interval_init"])
            if interval_init > 7:
                send_ok_response = False
        if "week_day" in json_data:
            week_day = json_data['week_day']
            if len(week_day) > 7:
                send_ok_response = False
        if "valves" in json_data:
            valves = json_data["valves"]
            for v in valves:
                if int(v["v"]) > 128:
                    send_ok_response = False
                if len(v["time"]) > 5:
                    send_ok_response = False
        if "from" and "to" in json_data:
            from_data = json_data['from']
            to_data = json_data['to']
            if len(from_data) > 5 or len(to_data) > 5:
                send_ok_response = False
        if (send_ok_response):
            json_data["id"] = 1
            json_data.pop('uuid')
            json_data.pop('client')
            msg = json.dumps(json_data)
            mqtt.publish(uuid+'/program/app',
                         msg, 0, False)
            return REQUEST_RESPONSE['OK'], 200
        else:
            return REQUEST_RESPONSE['PUBLISH_ERROR'], 407
    else:
        return REQUEST_RESPONSE['CLIENT_ERROR'], 406

@app.route('/api/sensors', methods=['GET'])
def get_sensor_data():
    #I have to received the following data: {"sensor_name":"sensor rarced wind"}
    if request.data:
        json_data = json.loads(request.data)
        # print(json_data)
        d = DatabaseInteractions()
        sensor_data = d.get_dataloger_sensor(str(json_data["sensor_name"]))
        if len(sensor_data) != 0:
            return json.dumps(sensor_data) 
        else:
            return "There is no sensor with this name", 400
    else:
        return REQUEST_RESPONSE['JSON_ERROR'], 400

if __name__ == '__main__':

    # cropstages = Cropstages()
    # cropstages.load_file('data/cropstages.json')
    # cropstages.calc_eta()
    # print(cropstages)
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)
    # app.run(host="0.0.0.0", port=80)
    mqtt.init_app(app)
