from db.adapters.base_adapter import BaseAdapter

class ApplicationModel:
    table_columns = None

    @classmethod
    def db_adapter(self):
        return BaseAdapter.get_instance()

    @classmethod
    def table_name(self):
        return self.__name__.lower() + 's'

    @classmethod
    def get_table_columns(self):
        if self.table_columns == None:
            self.table_columns = self.db_adapter().table_columns(self.table_name())
        return self.table_columns

    @classmethod
    def find(self, id):
        return self.db_adapter().find(self.table_name(), id)