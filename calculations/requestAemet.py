from credential import AEMET_KEY
import requests
import json
import datetime
import math


class RequestAemet(object):
    def __init__(self):
        # get them from Aemet:
        self.t_med = 0.0
        self.t_medprevious = 0.0
        self.t_max = 0.0
        self.t_min = 0.0
        self.hum_max = 0.0
        self.hum_min = 0.0
        self.hum_med = 0.0
        self.wind_speed = 0  # in km/hour

        self.rad_net = 0.0
        self.rad_solar = 0.0  # still do not know hoy to get it
        self.rad_solar_0 = 0.1

        self.height = 860.0  # in meters
        self.presure_atm = 0.0
        self.latitude = 42.34106

    def get_weather_params(self):
        url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/"
        url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/09059"  # for burgos
        querystring = {"api_key": AEMET_KEY}
        response = requests.request(
            "GET", url, headers={'cache-control': "no-cache"}, params=querystring)
        json_response = json.loads(response.text)
        # print(json_response)
        response = requests.request('GET', json_response['datos'])
        json_response = json.loads(response.text)
        # print(json.dumps(json_response, indent=5))
        # print(json.dumps(json_response['prediccion']['dia'][0]['probPrecipitacion'], indent=5))
        temp_max_min = []
        hum_max_min = []
        t_med = []
        wind_speed = []
        for prov in json_response:
            for i in range(1):
                data_temp = prov['prediccion']['dia'][i]['temperatura']
                temp_max_min.append((data_temp['minima'], data_temp['maxima']))
                data_temp = prov['prediccion']['dia'][i]['humedadRelativa']
                hum_max_min.append((data_temp['minima'], data_temp['maxima']))
                data_temp = prov['prediccion']['dia'][i]['temperatura']['dato']
                for d in data_temp:
                    t_med.append(d['value'])
                data_temp = prov['prediccion']['dia'][i]['viento']
                for v in data_temp:
                    wind_speed.append(v['velocidad'])
        # print(json.dumps(prov['prediccion']['dia'][0], indent=4))
        self.t_max = temp_max_min[0][0]
        self.t_min = temp_max_min[0][1]
        self.t_med = sum(t_med)/len(t_med)
        self.hum_max = hum_max_min[0][0]
        self.hum_min = hum_max_min[0][1]
        self.wind_speed = sum(wind_speed)/len(wind_speed)
        return (self.t_max,
                self.t_min,
                self.t_med,
                self.hum_max,
                self.hum_min,
                self.wind_speed)

    def get_open_data(self):
        url = "https://opendata.aemet.es/opendata/api/mapasygraficos/analisis"  # for burgos
        querystring = {"api_key": AEMET_KEY}
        response = requests.request(
            "GET", url, headers={'cache-control': "no-cache"}, params=querystring)

        json_response = json.loads(response.text)
        print(json.dumps(json_response, indent=4))
        print(json_response['datos'])
        response = requests.request('GET', json_response['datos'])
        # json_response = json.loads(response.text)
