import os
import tempfile
import unittest
import shutil
from booyah.extensions.string import String
from booyah.framework import Booyah

PROD_DB_PASSWORD = "pwd_from_env"
DEFAULT_DB_PASSWORD = "default_pwd"
BOOYAH_ENV = 'test'
TEST_DB_HOST = "host_test"

class TestFramework(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        os.environ['BOOYAH_LIB_TEST'] = ''
        self.previous_dir = os.getcwd()
        self.temp_dir = tempfile.mkdtemp()
        os.chdir(self.temp_dir)
        self.folder_name = os.path.basename(self.temp_dir)
        self.create_version_file()
        self.create_env_file()
        self.create_application_yaml()
        Booyah.configure()
    
    @classmethod
    def create_version_file(self):
        file_path = os.path.join(self.temp_dir, '.booyah_version')
        with open(file_path, 'w') as file:
            file.write("99.99.99")

    @classmethod
    def create_env_file(self):
        file_path = os.path.join(self.temp_dir, '.env')
        with open(file_path, 'w') as file:
            file.write(f"""
DB_PASSWORD={PROD_DB_PASSWORD}
BOOYAH_ENV={BOOYAH_ENV}
            """)
    
    @classmethod
    def create_application_yaml(self):
        yaml_content = f"""
defaults:
    database: &database
        host: localhost
        port: 5432
        adapter: postgresql
        database: booyah
        username: postgres
        password: {DEFAULT_DB_PASSWORD}
test:
    database:
        <<: *database
        host: {TEST_DB_HOST}
        port: 5432
        adapter: postgresql
        database: booyah
development:
    database:
        <<: *database
        host: localhost
        port: 5432
        adapter: postgresql
        database: booyah
production:
    database:
        <<: *database
        host: $DB_HOST
        port: 5432
        adapter: postgresql
        database: booyah_production
        username: $DB_USERNAME
        password: {PROD_DB_PASSWORD}
        """

        self.config_folder = os.path.join(self.temp_dir, 'config')
        os.makedirs(self.config_folder)

        file_path = os.path.join(self.config_folder, 'application.yml')
        with open(file_path, 'w') as file:
            file.write(yaml_content)

    @classmethod
    def tearDownClass(self):
        os.environ['BOOYAH_LIB_TEST'] = 'yes'
        os.chdir(self.previous_dir)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_get_version(self):
        assert Booyah.version == "99.99.99"
    
    def test_root(self):
        assert self.temp_dir in Booyah.root
    
    def test_name(self):
        assert Booyah.name == String(os.path.basename(self.temp_dir)).titleize()
    
    def test_anchor_yaml(self):
        assert Booyah.config['development']['database']['password'] == DEFAULT_DB_PASSWORD
    
    def test_env_in_yaml(self):
        assert Booyah.config['production']['database']['password'] == PROD_DB_PASSWORD
    
    def test_environment(self):
        assert Booyah.environment == BOOYAH_ENV

    def test_is_environment(self):
        assert Booyah.is_test == True
        assert Booyah.is_development == False
        assert Booyah.is_production == False
    
    def test_env_config(self):
        assert Booyah.env_config['database']['host'] == TEST_DB_HOST