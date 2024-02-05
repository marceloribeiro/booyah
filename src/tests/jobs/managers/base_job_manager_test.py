import unittest
import tempfile
import os
import shutil
from booyah.jobs.managers.base_job_manager import BaseJobManager
from booyah.framework import Booyah

class TestBaseJobManager(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.previous_dir = os.getcwd()
        self.temp_dir = tempfile.mkdtemp()
        os.chdir(self.temp_dir)
        Booyah.root = self.temp_dir
        app_jobs_dir = os.path.join(Booyah.root, 'app', 'jobs')
        os.makedirs(app_jobs_dir, exist_ok=True)
        for file_name in ['job_base.py', 'user_job.py', 'hello_job.py', 'other_job.py']:
            file_path = os.path.join(app_jobs_dir, file_name)
            with open(file_path, 'w'):
                pass


    @classmethod
    def tearDownClass(self):
        os.environ['BOOYAH_LIB_TEST'] = 'yes'
        os.chdir(self.previous_dir)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        Booyah.configure()

    def test_project_job_files(self):
        files = BaseJobManager().project_job_files()
        assert len(files) == 3
        assert 'user_job.py' in files
        assert 'hello_job.py' in files
        assert 'other_job.py' in files