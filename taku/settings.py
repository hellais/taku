import json

class Config(object):
    def __init__(self, config_file="taku.conf"):
        with open(config_file) as f:
            config = json.load(f)
        for k, v in config.items():
            setattr(self, k, v)

config = Config()
