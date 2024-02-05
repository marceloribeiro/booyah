import os
from booyah.framework import Booyah

class BaseJobManager:
    
    def instance(self):
        raise NotImplementedError("Subclasses must implement manager.")
    
    def project_job_files(self):
        folder_path = os.path.join(Booyah.root, 'app/jobs')

        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            raise ValueError(f"The path folder_path does not exist.")

        file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('job.py')]
        return file_names
