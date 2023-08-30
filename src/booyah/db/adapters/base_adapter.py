import os
from booyah.extensions.string import String

class BaseAdapter:
    @staticmethod
    def get_instance():
        adapter = String(os.getenv('DB_ADAPTER'))
        module_name = f'booyah.db.adapters.{adapter}.{adapter}_adapter'
        adapter_class = String(adapter + '_adapter').camelize()
        adapter_module = __import__(module_name, fromlist=[adapter_class])
        adapter_class = getattr(adapter_module, adapter_class)
        return adapter_class.get_instance()