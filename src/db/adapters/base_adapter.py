import os
from lib.helpers.application_helper import to_camel_case

class BaseAdapter:
    @staticmethod
    def get_instance():
        adapter = os.getenv('DB_ADAPTER')
        adapter_class = adapter + '_adapter'
        adapter_module = __import__('db.adapters.' + adapter_class, fromlist=[adapter_class])
        adapter_class = getattr(adapter_module, to_camel_case(adapter_class))

        return adapter_class.get_instance()