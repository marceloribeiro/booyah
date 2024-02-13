import os
import sys
import confuse
from booyah.extensions.string import String
from py_dotenv import read_dotenv

class Booyah:
    @classmethod
    def initial_config(self):
        self.is_booyah_project = False
        self.version = '0.0.1'
        self.is_lib_test = os.getenv('BOOYAH_LIB_TEST') == 'yes'
        if not self.is_lib_test:
            try:
                with open('.booyah_version', 'r') as version_file:
                    self.version = version_file.read().strip()
                self.is_booyah_project = True
            except FileNotFoundError:
                print(
                    "Error: This directory does not seem to be a Booyah project.\n"
                    "Please make sure you are in the correct directory or initialize a new Booyah project."
                )
        self.root = os.getcwd()
        self.folder_name = String(os.path.basename(os.getcwd()))
        self.name = self.folder_name.titleize()

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
    def add_project_module_if_needed(self):
        if not self.is_booyah_project:
            return
        try:
            __import__(Booyah.folder_name)
            return True
        except ImportError:
            sys.path.append(os.path.dirname(Booyah.root))
            return False

    @classmethod
    def configure(self):
        self.initial_config()
        if not (os.getenv('GITHUB_RUNNER') == 'yes'):
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
