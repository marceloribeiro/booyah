from booyah.session.session_manager import SessionManager
from booyah.models.session_storage import SessionStorage
from datetime import timedelta, datetime
import unittest
from booyah.session.storages.database_storage import DatabaseStorage
import json

DEFAULT_DATA = {'name': 'johndoe'}

class TestSessionManager(unittest.TestCase):
    def create_table_and_record(self):
        SessionStorage.drop_table()
        SessionStorage.create_table({
            'id': 'primary_key',
            'session_id': 'string',
            'data': 'text',
            'expires_at': 'datetime',
            'created_at': 'datetime',
            'updated_at': 'datetime'
        })
        record_params = {'session_id': 'abc', 'data': json.dumps({'name': 'johndoe'}), 'expires_at': datetime.utcnow() + timedelta(days=1)}
        record = SessionStorage(record_params)
        record.save()
        return record
        
    def test_init_default_storage(self):
        assert isinstance(SessionManager().storage, DatabaseStorage)
    
    def test_get_session(self):
        record = self.create_table_and_record()
        assert SessionManager().get_session(record.session_id) == {'name': 'johndoe'}
    
    def test_delete_session(self):
        record = self.create_table_and_record()
        SessionManager().delete_session(record.session_id)
        assert SessionManager().get_session(record.session_id) == {}

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
        assert json.loads(last_record.data) == DEFAULT_DATA
