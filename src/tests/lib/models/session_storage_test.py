from booyah.models.session_storage import SessionStorage
from datetime import datetime, timedelta

class TestSessionStorage:

    def test_is_expired(self):
        record = SessionStorage()
        expired_date = datetime.utcnow() - timedelta(days=1)
        record.expires_at = expired_date
        assert record.is_expired()

    def test_is_not_expired(self):
        record = SessionStorage()
        expired_date = datetime.utcnow() + timedelta(days=1)
        record.expires_at = expired_date
        assert record.is_expired() == False