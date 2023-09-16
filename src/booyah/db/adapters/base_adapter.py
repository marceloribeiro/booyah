import os
from booyah.extensions.string import String
import subprocess

class BaseAdapter:
    @staticmethod
    def get_instance():
        adapter = String(os.getenv('DB_ADAPTER'))
        module_name = f'booyah.db.adapters.{adapter}.{adapter}_adapter'
        adapter_class = (adapter + '_adapter').camelize()
        adapter_module = __import__(module_name, fromlist=[adapter_class])
        adapter_class = getattr(adapter_module, adapter_class)
        return adapter_class.get_instance()
    
    @staticmethod
    def open_client():
        adapter = os.getenv('DB_ADAPTER', 'postgresql')
        db_client_command = None
        if adapter == 'postgresql':
            db_client_command = f"PGPASSWORD={os.getenv('DB_PASSWORD')} psql -U {os.getenv('DB_USERNAME')} {os.getenv('DB_DATABASE')}"
        if db_client_command:
            subprocess.call(db_client_command, shell=True)