from booyah.jobs.managers.celery_job_manager import CeleryJobManager

class JobsManager:
    def __init__(self, manager=None):
        if not manager:
            self.manager = CeleryJobManager()
        else:
            self.manager = manager

jobs_manager = JobsManager()
celery = jobs_manager.manager.instance()