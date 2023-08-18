from db.adapters.base_adapter import BaseAdapter

EQUAL_OPERATOR = '= ?'
LIKE_OPERATOR = 'like ?'
DIFFERENT_OPERATOR = '!= ?'
GREATER_THAN_OPERATOR = '> ?'
GREATER_THAN_OR_EQUAL_OPERATOR = '>= ?'
LESS_THAN_OPERATOR = '< ?'
LESS_THAN_OR_EQUAL_OPERATOR = '<= ?'
QUERY_OPERATORS = {
    'eq': EQUAL_OPERATOR,
    'like': LIKE_OPERATOR,
    'not_like': DIFFERENT_OPERATOR,
    'gt': GREATER_THAN_OPERATOR,
    'gte': GREATER_THAN_OR_EQUAL_OPERATOR,
    'lt': LESS_THAN_OPERATOR,
    'lte': LESS_THAN_OR_EQUAL_OPERATOR
}

class ModelQueryBuilder:
    def __init__(self, model_class):
        self.model_class = model_class
        self.selected_attributes = []
        self.select_query = ''
        self.where_conditions = []
        self.joins = []
        self.order_by_attributes = []
        self.group_by_attributes = []
        self.limit = None
        self.offset = None
        self.scope = None
        self.db_adapter = BaseAdapter.get_instance()

    def all(self):
        self.select_all_columns()
        return self

    def find(self, id):
        self.select_all_columns()
        self.where(f"{self.model_class.table_name()}.id = {id}")
        return self

    def select_all_columns(self):
        columns = map(lambda column: f"{self.model_class.table_name()}.{column}", self.model_class.get_table_columns())
        self.select(", ".join(columns))
        self

    def select(self, *args):
        self.selected_attributes += args
        self.select_query = f"SELECT {','.join(self.selected_attributes)} FROM {self.model_class.table_name()}"
        return self

    def where(self, *args):
        condition = f"{args[0]}"
        if len(args) > 1:
            for operator in QUERY_OPERATORS.values():
                if operator in condition:
                    condition = condition.replace(' ?', f" {self.quote_if_needed(args[1])}")
                    self.where_conditions.append(condition)
                    return self
            condition = f"{condition} = {self.quote_if_needed(args[1])}"
        self.where_conditions.append(condition)
        return self

    def quote_if_needed(self, value):
        if isinstance(value, str):
            return f"'{value}'"
        return value

    def build_query(self):
        if self.select_query == '':
            self.select_all_columns()
        query = self.select_query

        if self.joins:
            query += ' ' + ' '.join(self.joins)
        if self.where_conditions:
            query += ' WHERE ' + ' AND '.join(self.where_conditions)
        if self.group_by_attributes:
            query += ' GROUP BY ' + ','.join(self.group_by_attributes)
        if self.order_by_attributes:
            query += ' ORDER BY ' + ','.join(self.order_by_attributes)
        if self.limit:
            query += f" LIMIT {self.limit}"
        if self.offset:
            query += f" OFFSET {self.offset}"
        return query

    def model_from_result(self, result):
        return self.model_class(dict(zip(self.model_class.get_table_columns(), result)))

    def results(self):
        full_query = self.build_query()
        raw_results = self.db_adapter.fetch(full_query)
        results = list(map(lambda result: self.model_from_result(result), raw_results))
        self.cleanup()
        return results

    def count(self):
        full_query = self.build_query()
        full_query = f"SELECT COUNT(*) FROM ({full_query}) AS count"
        raw_results = self.db_adapter.fetch(full_query)
        self.cleanup()
        return raw_results[0][0]

    def first(self):
        self.limit = 1
        results = self.results()
        if results:
            return results[0]
        return None

    def last(self):
        results = self.results()
        if results:
            return results[len(results) - 1]
        return None

    def each(self, callback):
        for result in self.results():
            callback(result)

    def cleanup(self):
        self.select_query = ''
        self.selected_attributes = []
        self.where_conditions = []
        self.joins = []
        self.order_by_attributes = []
        self.group_by_attributes = []
        self.limit = None
        self.offset = None
        self.scope = None

    # Iteratable methods
    def __iter__(self):
        self.current_index = 0
        self._results = self.results()
        return self

    def __next__(self):
        try:
            result = self._results[self.current_index]
        except IndexError:
            raise StopIteration
        self.current_index += 1
        return result

    def __len__(self):
        return len(self.results())

    def __getitem__(self, key):
        return self.results()[key]

    def __setitem__(self, key, value):
        self.results()[key] = value

    def __delitem__(self, key):
        del self.results()[key]

    def __contains__(self, item):
        return item in self.results()

    def __reversed__(self):
        return reversed(self.results())