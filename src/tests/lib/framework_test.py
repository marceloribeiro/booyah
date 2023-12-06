import os
import tempfile
import unittest
import shutil

class TestFramework(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.previous_dir = os.getcwd()
        self.temp_dir = tempfile.mkdtemp()
        os.chdir(self.temp_dir)
        self.folder_name = os.path.basename(self.temp_dir)
        self.create_version_file()
        self.create_env_file()
        self.create_application_yaml()
    
    @classmethod
    def create_version_file(self):
        file_path = os.path.join(self.temp_dir, '.booyah_version')
        with open(file_path, 'w') as file:
            file.write("99.99.99")

    @classmethod
    def create_env_file(self):
        file_path = os.path.join(self.temp_dir, '.env')
        with open(file_path, 'w') as file:
            file.write("DB_PASSWORD=pwd_from_env")
    
    @classmethod
    def create_application_yaml(self):
        yaml_content = """
defaults:
    database: &database
        host: localhost
        port: 5432
        adapter: postgresql
        database: booyah
        username: postgres
        password: defaultpwd
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
        password: $DB_PASSWORD
        """

        self.config_folder = os.path.join(self.temp_dir, 'config')
        os.makedirs(self.config_folder)

        file_path = os.path.join(self.config_folder, 'application.yml')
        with open(file_path, 'w') as file:
            file.write(yaml_content)

    @classmethod
    def tearDownClass(self):
        os.chdir(self.previous_dir)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_get_version(self):
        from booyah.framework import Booyah
        assert Booyah.version == "99.99.99"