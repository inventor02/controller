import yaml

class Config:
    def __init__(self):
        self.config = None
        self.load_config()

    def load_config(self):
        with open("config.yaml", "r") as file:
            self.config = yaml.safe_load(file)

    def get(self, key):
        return self.config[key]
