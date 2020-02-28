# config.py

import yaml

labels = [
    ('storageFolder', str),
    ('secretKey', str),
    ('extensions', list),
]


class Config():

    def __init__(self):
        self.configuration = {}
        # Open and read config file
        try:
            with open('config.yaml', 'r') as f:
                configFile = f.read()
            rawConfig = yaml.load(configFile, Loader=yaml.BaseLoader) or {}
        except FileNotFoundError:
            print('No config.yaml file found!')
            exit(1)

        for l in labels:
            try:
                if not isinstance(rawConfig[l[0]], l[1]):

                    raise KeyError
                self.configuration[l[0]] = rawConfig[l[0]]
            except KeyError:
                print(f'No {l[0]} found!')
                exit(1)

    def getConfiguration(self):
        return self.configuration
