from booyah.models.session_storage import SessionStorage
from datetime import datetime, timedelta

class TestSessionStorage:

    def create_session_storage_table(self):
        SessionStorage.drop_table()
        SessionStorage.create_table({
            'id': 'primary_key',
            'session_id': 'string',
            'data': 'text',
            'expires_at': 'datetime',
            'created_at': 'datetime',
            'updated_at': 'datetime'
        })

    def test_is_expired(self):
        self.create_session_storage_table()
        record = SessionStorage()
        expired_date = datetime.utcnow() - timedelta(days=1)
        record.expires_at = expired_date
        assert record.is_expired()

    def test_is_not_expired(self):
        self.create_session_storage_table()
        record = SessionStorage()
        expired_date = datetime.utcnow() + timedelta(days=1)
        record.expires_at = expired_date
        assert record.is_expired() == False