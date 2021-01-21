import secrets
import json

# I have each uuid associated with each client
## UUID : CLIENT


# This is a data class to store in a structured way:
class AssociationUuidClient(object):
    def __init__(self, client, uuid):
        self.client = client
        self.uuid = []
        # It does not matter if I received a list or a simple string:
        if isinstance(uuid, list):
            for u in uuid:
                self.uuid.append(u)
        else:
            self.uuid.append(uuid)

    def __repr__(self):
        data_response = str(self.client) + " - " + str(self.uuid)
        return data_response

# I store all the clients and keys and check if the post is correct


class Apikey (object):
    def __init__(self):
        # Store the association uuid inside this class
        self.association_uuid_client = []
        # Load this association from a file first

    def load_asssociation(self, file):
        try:
            with open(file) as json_file:
                data = json.load(json_file)
                for r in data['requests']:
                    client_uuid = AssociationUuidClient(r['client'], r['uuid'])
                    self.association_uuid_client.append(client_uuid)
        except:
            raise Exception("Unable to load the file on the route:  " + file)

    def generate_key(self, length):
        return secrets.token_urlsafe(length)

    def check_if_associated(self, uuid, client):
        # This is not very eficient but for now the number of clients is not very high:
        for c in self.association_uuid_client:
            if client in c.client:
                # print("The client exist")
                for u in c.uuid:
                    if uuid == u:
                        # print("Match the uuid")
                        return True
                else:
                    # print("This client does not have this uuid")
                    return False
        else:
            return False
    def __repr__(self):
        return_data = ""
        for d in self.association_uuid_client:
            return_data+=d.client + " -> "
            for u in d.uuid:
                return_data+= u + ', '
            return_data += '\n'
        return (return_data)

    

def test_api_key():
    data_keys = Apikey()
    data_keys.load_asssociation('data/uuid_client.json')
    random_client = ["hola", "acua_client"]
    random_uuid = "Xxfs9g510gvBXP7YGjRGMg"
    print(data_keys)

# test_api_key()
