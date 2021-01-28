import json
import requests
import time
from credential import *

# Making a POST request to this urls:
urls = [
    "/api/manprog",
    "/api/manvalve",
    "/api/program",
    "/api/general",
    "/api/stop"
]

et0_json = {
    "t_med": 15.11,
    "t_medprevious": 14.8,
    "t_max": 22.73,
    "t_min": 8.35,
    "hum_max": 53.4,
    "hum_min": 25.05,
    "hum_med": 41.1,
    "rad_solar": 21.37,
    "wind_speed": 12.744,
    "height":371.0,
    "latitude": 39.8152777
}

j = json.dumps(et0_json)
r = requests.get(SERVER + '/cal_etc', j)
print(r)
# for index, req in enumerate(all_requests_jsons):
#     j = json.dumps(req)
#     r = requests.post(SERVER + urls[index], j)
#     print(r)
#     time.sleep(0.1)
