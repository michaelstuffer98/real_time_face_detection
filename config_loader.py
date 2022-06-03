import json

class ConfigLoader:
    def __init__(self):
        with open("config.json") as f:
            self.config = json.load(f)

    def get(self, ressource):
        return self.config[ressource]

    def set(self, ressource, value):
        self.config[ressource] == value

    def __getitem__(self, key):
        return self.config[key]