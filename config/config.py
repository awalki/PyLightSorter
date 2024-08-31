import configparser

class ConfigManager:

    def __init__(self, config_path):
        self.file_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def read_key(self, section, key):
        return self.config[section][key]

    def read_keys(self, section):
        cfg = self.config[section]

        return cfg

    def change_key(self, section, key, value):
        self.config[section][key] = value
        self.save()

    def save(self):
        with open(self.file_path, 'w') as file:
            self.config.write(file)