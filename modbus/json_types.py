import json


class ReadRequest:

    def __init__(self, address: int, count=1):
        self.address = address
        self.count = count

    def toJSON(self):
        return json.dumps({
            "request": "read",
            "payload": {
                "address": self.address,
                "count": self.count
            }
        })

    @staticmethod
    def fromJSON(data):
        req = data["payload"]
        return ReadRequest(req["address"], req["count"])


class WriteRequest:

    def __init__(self, address: int, values):
        self.address = address
        self.values = values

    def toJSON(self):
        return json.dumps({
            "request": "write",
            "payload": {
                "address": self.address,
                "values": self.values
            }
        })

    @staticmethod
    def fromJSON(data):
        req = data["payload"]
        return WriteRequest(req["address"], req["values"])
