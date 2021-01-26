from credential import AEMET_KEY
import requests 
import json

class RequestAemet(object):
    def __init__(self):
        self.t_med = 15.0
        self.t_medprevious = 0.0
        self.t_max = 20.0
        self.t_min = 10.0
        self.rad_net = 0.0
        self.rad_solar = 0.0  # obtein from api
        self.rad_solar_0 = 0.1
        self.height = 800.0  # in meters
        self.hum_max = 0.0
        self.hum_min = 0.0
        self.presure_atm = 0.0
        self.latitude = 0
        self.days = 0
        self.wind_speed = 8  # in km/hour
    def __repr__(self):
        return self.t_med

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
        # print(json.dumps(json_response['prediccion']['dia'][0]['probPrecipitacion'], indent=5))
        temp_max_min = []
        hum_max_min = []
        t_med = []
        for prov in json_response:
            for i in range(1):
                data_temp = prov['prediccion']['dia'][i]['temperatura']
                temp_max_min.append((data_temp['minima'], data_temp['maxima']))
                data_temp = prov['prediccion']['dia'][i]['humedadRelativa']
                hum_max_min.append((data_temp['minima'], data_temp['maxima']))
                data_temp = prov['prediccion']['dia'][i]['temperatura']['dato']
                for d in data_temp:
                    t_med.append(d['value'])
        # print(json.dumps(prov['prediccion']['dia'][1], indent=4))
        print(t_med)
        self.t_max = temp_max_min[0][0]
        self.t_min =temp_max_min[0][1]
        self.hum_max = temp_max_min[0][0]
        self.hum_min = hum_max_min[0][1]
        return self.t_max, self.t_min, self.hum_max, self.hum_min


    def weather_radars(self):
        url = "https://opendata.aemet.es/opendata/api/red/radar/nacional"  # for burgos
        querystring = {"api_key": AEMET_KEY}
        response = requests.request(
            "GET", url, headers={'cache-control': "no-cache"}, params=querystring)
        json_response = json.loads(response.text)
        print(json_response['datos'])
        response = requests.request('GET', json_response['datos'])
        # json_response = json.loads(response.text)
        
        print(response.text)