import os
import sys
from booyah.helpers.application_helper import to_camel_case
from booyah.db.adapters.postgresql_adapter import PostgresqlAdapter

class BaseAdapter:
    @staticmethod
    def get_instance():
        adapter = os.getenv('DB_ADAPTER')
        adapter_class = adapter + '_adapter'
        adapter_class = getattr(sys.modules[__name__], to_camel_case(adapter_class))

        return adapter_class.get_instance()