import json
import requests
from credential import SERVER, data_to_send

# Making a POST request:
json = json.dumps(data_to_send)

r = requests.post(SERVER + "/api/manvalve", json)
print(r) #status code
# print content of request
# print(r.json())
