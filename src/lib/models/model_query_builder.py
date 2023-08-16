from db.adapters.base_adapter import BaseAdapter
import json

class ModelQueryBuilder:
    def __init__(self, model_class):
        self.model_class = model_class
        self.selected_attributes = []
        self.select_query = ''
        self.where_conditions = []
        self.joins = []
        self.order_by_attributes = []
        self.group_by_attributes = []
        self.limit_amount = None
        self.offset_amount = None
        self.scope = None
        self.db_adapter = BaseAdapter.get_instance()

    def all(self):
        columns = map(lambda column: f"{self.model_class.table_name()}.{column}", self.model_class.get_table_columns())
        self.select(", ".join(columns))
        return self

    def select(self, *args):
        self.selected_attributes += args
        self.select_query = f"SELECT {','.join(self.selected_attributes)} FROM {self.model_class.table_name()}"
        return self

    def build_query(self):
        query = self.select_query
        if self.joins:
            query += ' ' + ' '.join(self.joins)
        if self.where_conditions:
            query += ' WHERE ' + ' AND '.join(self.where_conditions)
        if self.group_by_attributes:
            query += ' GROUP BY ' + ','.join(self.group_by_attributes)
        if self.order_by_attributes:
            query += ' ORDER BY ' + ','.join(self.order_by_attributes)
        if self.limit_amount:
            query += f" LIMIT {self.limit_amount}"
        if self.offset_amount:
            query += f" OFFSET {self.offset_amount}"
        return query

    def model_from_result(self, result):
        return self.model_class(dict(zip(self.model_class.get_table_columns(), result)))

    def results(self):
        full_query = self.build_query()
        raw_results = self.db_adapter.fetch(full_query)
        results = list(map(lambda result: self.model_from_result(result), raw_results))
        return results