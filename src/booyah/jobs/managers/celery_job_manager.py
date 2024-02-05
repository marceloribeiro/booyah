from celery import Celery
from booyah.framework import Booyah
from booyah.jobs.managers.base_job_manager import BaseJobManager

DEFAULT_BROKER = 'redis://localhost:6379/0'
DEFAULT_PROJECT = 'booyah'

class CeleryJobManager(BaseJobManager):
    def __init__(self):
        Booyah.add_project_module_if_needed()
        self.load_config()
        self.app = Celery(
            self.project_name,
            broker=self.broker,
            include=self.jobs_to_include()
        )
    
    def load_config(self):
        self.project_name = DEFAULT_PROJECT
        self.broker = DEFAULT_BROKER
        if not Booyah.is_booyah_project:
            self.project_name = Booyah.folder_name if not Booyah.env_config['jobs']['name'] else Booyah.env_config['jobs']['name']
            self.broker = Booyah.env_config['jobs']['broker']

    def jobs_to_include(self):
        job_files = self.project_job_files()
        includes = ['booyah.jobs.sessions_job']
        for job_file in job_files:
            includes.append(Booyah.folder_name + '.app.jobs.' + job_file.replace('.py', ''))
        return includes
    
    def instance(self):
        return self.app