import os
import unittest
import tempfile
from datetime import datetime
from booyah.generators.helpers.path import new_migration_file_path

class TestHelperPath(unittest.TestCase):
    def setUp(self):
        script_path = os.path.abspath(__file__)
        test_folder = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
        self.target_folder = os.path.join(test_folder, 'db', 'migrate')
        self.temp_file = None

    def tearDown(self):
        if self.temp_file:
            os.remove(self.temp_file)

    def test_new_migration_file_path(self):
        new_file_path = new_migration_file_path(self.target_folder, 'migrationname.py')
        file_parts = new_file_path.split('_')
        assert file_parts[-1] == "migrationname.py"
        assert self.target_folder in file_parts[0]
        assert file_parts[0].split('/')[-1][0:8] == datetime.strftime(datetime.now(), '%Y%m%d')
        
        self.temp_file = new_file_path
        with open(self.temp_file, 'w') as file:
            file.write('Migration content')
        new_file_path = new_migration_file_path(self.target_folder, 'migrationname.py')
        file_parts2 = new_file_path.split('_')
        assert file_parts[0].split('/')[-1] != file_parts2[0].split('/')[-1]