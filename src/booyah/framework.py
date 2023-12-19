import os
import confuse
from booyah.extensions.string import String
from py_dotenv import read_dotenv

class Booyah:
    @classmethod
    def initial_config(self):
        self.version = '0.0.0'
        self.is_lib_test = os.getenv('BOOYAH_LIB_TEST') == 'yes'
        if not self.is_lib_test:
            try:
                with open('.booyah_version', 'r') as version_file:
                    self.version = version_file.read().strip()
            except FileNotFoundError:
                print(
                    "Error: This directory does not seem to be a Booyah project.\n"
                    "Please make sure you are in the correct directory or initialize a new Booyah project."
                )
        self.root = os.getcwd()
        self.folder_name = String(os.path.basename(os.getcwd()))
        self.name = String(os.path.basename(os.getcwd())).titleize()

    @classmethod
    def substitute_env_variables(self, config):
        for key, value in config.items():
            real_value = value.get()
            if isinstance(real_value, dict):
                Booyah.substitute_env_variables(value)
            elif isinstance(real_value, str):
                config[key] = os.path.expandvars(real_value)
    
    @classmethod
    def config_to_dict(self, config):
        result = {}
        for key, value in config.items():
            real_value = value.get()
            if isinstance(real_value, dict):
                result[key] = Booyah.config_to_dict(value)
            else:
                result[key] = real_value
        return result

    @classmethod
    def configure(self):
        self.initial_config()
        try:
            read_dotenv('.env' if not self.is_lib_test else 'tests/.env.test')
        except:
            print('.env file not found')
        self.getenv = os.getenv
        self.environment = os.getenv('BOOYAH_ENV') or 'development'
        self.is_development = self.environment == 'development'
        self.is_test = self.environment == 'test'
        self.is_production = self.environment == 'production'

        config = confuse.Configuration(Booyah.name.classify())
        if not self.is_lib_test:
            config.set_file(os.path.join(Booyah.root, 'config', 'application.yml'))
        else:
            config.set_file(os.path.join(Booyah.root, 'tests', 'application.yml'))
        Booyah.substitute_env_variables(config)
        config_dict = Booyah.config_to_dict(config)

        if self.environment and self.environment in config_dict:
            self.env_config = config_dict[self.environment]
        else:
            self.env_config = {}
        self.config = config_dict

Booyah.configure()