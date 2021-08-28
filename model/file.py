import json
import os


class File:
    def getJson(self):
        if not os.path.isfile('data/mdp.json'):
            # open('data/mdp.json', "x")
            newJson = {"MainPassword": "gAAAAABhKNqjP3HM2veXVAH_eOSVOLAYxkWzufrZzjuFU6ZmuN9UGcTwMO_Bo7M4c39yg77JlzobL9czOslnmgaVec-dK16N0g==", "Applications": {}}
            self.setJson(newJson)

        with open('data/mdp.json') as file:
            return json.load(file)

    def setJson(self, data):
        with open('data/mdp.json', 'w') as file:
            json.dump(data, file, indent=4)
