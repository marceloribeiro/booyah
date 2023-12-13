from booyah.session.storages.database_storage import DatabaseStorage
from booyah.cookies.cookies_manager import cookies_manager

class SessionManager:
    def __init__(self, storage=None):
        if not storage:
            self.storage = DatabaseStorage()
        else:
            self.storage = storage

    def get_session(self, session_id):
        return self.storage.get_session_dict(session_id)

    def delete_session(self, session_id):
        self.storage.destroy_session(session_id)

    def save_session(self):
        session_id = cookies_manager.get_cookie('sessionid')
        expiration = cookies_manager.expiration_date('sessionid')
        self.storage.save_session(session_id, self.session, expiration)
    
    def from_cookie(self):
        self.session = self.get_session(cookies_manager.get_cookie('sessionid'))
        return self.session

session_manager = SessionManager()