import json
import os


class File:
    def getJson(self):
        if not os.path.isdir("data/"):
            os.mkdir("data/")
        if not os.path.isfile('data/mdp.json'):
            open('data/mdp.json', "x")
            newJson = {"MainPassword": "gAAAAABhLVEfytuDPiu2FaBQEeU95eV1Kt4eC82U_KOByWm3RvOlzlaXQz7xhuHzKCFclTYpPHfJIO3Ptkm6bw2Bu4Z_irMw1g==", "Applications": {}}
            self.setJson(newJson)

        with open('data/mdp.json') as file:
            return json.load(file)

    def setJson(self, data):
        with open('data/mdp.json', 'w') as file:
            json.dump(data, file, indent=4)
