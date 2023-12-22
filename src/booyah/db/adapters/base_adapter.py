import os
from booyah.extensions.string import String
import subprocess
from booyah.framework import Booyah

class BaseAdapter:
    @staticmethod
    def get_instance():
        db_config = Booyah.env_config['database']
        adapter = String(db_config['adapter'])
        module_name = f'booyah.db.adapters.{adapter}.{adapter}_adapter'
        adapter_class = (adapter + '_adapter').camelize()
        adapter_module = __import__(module_name, fromlist=[adapter_class])
        adapter_class = getattr(adapter_module, adapter_class)
        return adapter_class.get_instance()
    
    @staticmethod
    def open_client():
        db_config = Booyah.env_config['database']
        adapter = db_config['adapter']
        db_client_command = None
        if adapter == 'postgresql':
            db_client_command = f"PGPASSWORD={db_config['password']} psql -U {db_config('username')} {db_config('database')}"
        if db_client_command:
            subprocess.call(db_client_command, shell=True)