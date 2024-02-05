import unittest
import json
from datetime import timedelta, datetime
from cryptography.fernet import Fernet
from booyah.models.session_storage import SessionStorage
from booyah.session.storages.database_storage import DatabaseStorage

class TestDatabaseStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.record_params = {
            'session_id': 'abc',
            'data': json.dumps({'name': 'johndoe'}),
            'expires_at': datetime.utcnow() + timedelta(days=1)
        }
        f = Fernet("D47Gc_fnWbAz84-eRZDcG0t3OW006UArBhR0_ZtDDHs=")
        self.record_params['data'] = f.encrypt(self.record_params['data'].encode('utf-8')).decode('utf-8')

    def test_clear_expired(self):
        SessionStorage.all().where('1=1').destroy_all()
        record = SessionStorage(self.record_params)
        record.save()
        self.record_params['session_id'] = 'def'
        self.record_params['expires_at'] = datetime.utcnow() - timedelta(days=1)
        expired_record = SessionStorage(self.record_params)
        expired_record.save()
        assert SessionStorage.count() == 2
        DatabaseStorage().clear_expired()
        assert SessionStorage.count() == 1
        