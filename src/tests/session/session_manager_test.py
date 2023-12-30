from booyah.session.session_manager import SessionManager
from booyah.models.session_storage import SessionStorage
from datetime import timedelta, datetime
import unittest
from booyah.session.storages.database_storage import DatabaseStorage
import json
from cryptography.fernet import Fernet

DEFAULT_DATA = {'name': 'johndoe'}

class TestSessionManager(unittest.TestCase):
    
    def create_table_and_record(self):
        self.session_key = "D47Gc_fnWbAz84-eRZDcG0t3OW006UArBhR0_ZtDDHs="
        record_params = {'session_id': 'abc', 'data': json.dumps({'name': 'johndoe'}), 'expires_at': datetime.utcnow() + timedelta(days=1)}
        f = Fernet(self.session_key)
        record_params['data'] = f.encrypt(record_params['data'].encode('utf-8')).decode('utf-8')
        record = SessionStorage(record_params)
        record.save()
        return record
        
    def test_init_default_storage(self):
        assert isinstance(SessionManager().storage, DatabaseStorage)
    
    def test_get_session(self):
        record = self.create_table_and_record()
        assert SessionManager().get_session(record.session_id, self.session_key) == {'name': 'johndoe'}
    
    def test_delete_session(self):
        record = self.create_table_and_record()
        SessionManager().delete_session(record.session_id)
        assert SessionManager().get_session(record.session_id, self.session_key) == {}

    def test_save_session(self):
        self.create_table_and_record()
        from booyah.cookies.cookies_manager import cookies_manager
        environment = {}
        cookies_manager.initialize(environment)
        session_id = cookies_manager.create_session()
        expiration = cookies_manager.expiration_date('sessionid')
        session_manager = SessionManager()
        session_manager.session = DEFAULT_DATA
        session_manager.save_session()
        last_record = SessionStorage.all().last()
        assert last_record.session_id == session_id
        assert last_record.expires_at == expiration
        key = cookies_manager.get_cookie('sessionkey')
        f = Fernet(key)
        data_str = f.decrypt(last_record.data.encode('utf-8')).decode('utf-8')
        assert json.loads(data_str) == DEFAULT_DATA
