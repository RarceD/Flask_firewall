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

for index, req in enumerate(all_requests_jsons):
    j = json.dumps(req)
    r = requests.post(SERVER + urls[index], j)
    print(r) 
    time.sleep(0.1)