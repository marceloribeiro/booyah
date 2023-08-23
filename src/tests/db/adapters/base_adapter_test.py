from booyah.db.adapters.base_adapter import BaseAdapter

class TestBaseAdapter:
    def test_get_instance(self):
        adapter = BaseAdapter.get_instance()
        assert adapter is not None
        assert adapter.__class__.__name__ == 'PostgresqlAdapter'