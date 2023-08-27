import os
from booyah.helpers.application_helper import to_camel_case

class BaseAdapter:
    @staticmethod
    def get_instance():
        adapter = os.getenv('DB_ADAPTER')
        module_name = f'booyah.db.adapters.{adapter}.{adapter}_adapter'
        adapter_class = to_camel_case(adapter + '_adapter')
        adapter_module = __import__(module_name, fromlist=[adapter_class])
        adapter_class = getattr(adapter_module, adapter_class)
        return adapter_class.get_instance()