from booyah.session.session_manager import session_manager
from booyah.models.session_storage import SessionStorage
from booyah.cookies.cookies_manager import cookies_manager
from datetime import timedelta, datetime
import unittest
import json
from cryptography.fernet import Fernet

class TestFlashMessage(unittest.TestCase):
    def init_cookies(self):
        self.session_id = 'abcdef'
        self.session_key = "D47Gc_fnWbAz84-eRZDcG0t3OW006UArBhR0_ZtDDHs="

        cookies_manager.initialize({})
        cookies_manager.set_cookie('sessionid', self.session_id)
        cookies_manager.set_cookie('sessionkey', self.session_key)

    def create_table_and_record(self):
        self.init_cookies()

        record_data = {'name': 'johndoe'}
        record_params = {
            'session_id': self.session_id,
            'data': json.dumps(record_data),
            'expires_at': datetime.utcnow() + timedelta(days=1)
        }
        
        f = Fernet(self.session_key)
        record_params['data'] = f.encrypt(record_params['data'].encode('utf-8')).decode('utf-8')
        record = SessionStorage(record_params)
        record.save()

        self.session = session_manager.from_cookie()
        self.flash = session_manager.flash_messages

    def test_set_item(self):
        self.create_table_and_record()
        text = 'This is a notice'
        self.flash['notice'] = text
        assert True if '_flash' in self.session else False
        assert self.session['_flash']['notice'] == text

    def test_get_item(self):
        self.create_table_and_record()
        text = 'This is a notice'
        self.flash['notice'] = text
        assert self.flash['notice'] == text

        # Enable to clean flash value
        self.flash.can_clean = True
        # Using/reading flash value will remove it from session
        assert self.flash['notice'] == text

        notice_in_flash = True if 'notice' in self.flash else False
        notice_in_session = True if 'notice' in self.session['_flash'] else False
        assert notice_in_flash == True
        assert notice_in_session == False

    def test_del_item(self):
        self.create_table_and_record()
        self.flash['notice'] = 'This is a notice'
        del self.flash['notice']

        notice_in_flash = True if 'notice' in self.flash else False
        notice_in_session = True if 'notice' in self.session['_flash'] else False

        assert notice_in_flash == False
        assert notice_in_session == False
    
    def test_flash_now(self):
        self.create_table_and_record()
        text = 'This is a notice'
        self.flash.now['notice'] = text
        notice_in_session = True if 'notice' in self.session['_flash'] else False
        notice_in_flash = True if 'notice' in self.flash else False
        assert notice_in_session == False
        assert notice_in_flash == True

        self.flash.can_clean = True
        assert self.flash['notice'] == text

        # after read the value
        notice_in_session = True if 'notice' in self.session['_flash'] else False
        notice_in_flash = True if 'notice' in self.flash else False

        assert notice_in_session == False
        assert notice_in_flash == True