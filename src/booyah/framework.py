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
    def substitute_env_variables(self, config):
        for key, value in config.items():
            real_value = value.get()
            if isinstance(real_value, dict):
                Booyah.substitute_env_variables(value)
            elif isinstance(real_value, str):
                config[key] = os.path.expandvars(real_value)
    
    @classmethod
    def confuse_to_dict(self, config):
        result = {}
        for key, value in config.items():
            real_value = value.get()
            if isinstance(real_value, dict):
                result[key] = Booyah.confuse_to_dict(value)
            else:
                result[key] = real_value
        return result

    @classmethod
    def configure(self):
        read_dotenv('.env')
        self.getenv = os.getenv
        self.environment = os.getenv('BOOYAH_ENV')
        self.is_development = self.environment == 'development'
        self.is_test = self.environment == 'test'
        self.is_production = self.environment == 'production'

        config = confuse.Configuration(Booyah.name.classify())
        config.set_file(os.path.join(Booyah.root, 'config', 'application.yml'))
        Booyah.substitute_env_variables(config)
        config_dict = Booyah.confuse_to_dict(config)

        if self.environment and self.environment in config_dict:
            self.env_config = config_dict[self.environment]
        else:
            self.env_config = {}
        self.config = config_dict

Booyah.configure()