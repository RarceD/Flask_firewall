# Flask_firewall
Simple firewall, received post, filter, check and publish via mqtt.

Every post must have a API KEY acording to the client, with this key it can only interact with their associated uuid's.

## Running:
 ```python
sudo pip install Flask
sudo pip install flask-mqtt
```

## Functionallity:
    [x] Received a post with a fix json format and a key.
    [X] Check if the user with this key is able to interact with this uuid.
    [ ] Sqlite python, for storing this associated information. 
    [x] Filter and discard wrong parameters and messages.
    [x] Inform of wrong request in order to re post it well.
    [x] Publish the information on the broker.
    [x] Visual part, the main page has a index.html public page on the server.
