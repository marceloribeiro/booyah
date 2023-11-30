import os
import confuse
from booyah.extensions.string import String
from py_dotenv import read_dotenv

with open('.booyah_version', 'r') as version_file:
    booyah_version = version_file.read().strip()

class Booyah:
    root = os.getcwd()
    folder_name = os.path.basename(os.getcwd())
    name = String(os.path.basename(os.getcwd())).titleize()
    version = booyah_version

    @classmethod
    def configure(self):
        read_dotenv('.env')
        self.getenv = os.getenv
        self.environment = os.getenv('BOOYAH_ENV')
        self.is_development = self.environment == 'development'
        self.is_test = self.environment == 'test'
        self.is_production = self.environment == 'production'

        config = confuse.Configuration(Booyah.name.classify())
        config.set_file(os.path.join(Booyah.root, 'config', 'application.yaml'))
        config_dict = {}

        for key, value in config.items():
            config_dict[key] = value.get()
        self.config = config_dict

Booyah.configure()