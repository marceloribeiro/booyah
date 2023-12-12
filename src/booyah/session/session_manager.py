import time
from booyah.session.storages.database_storage import DatabaseStorage

class SessionManager:
    def __init__(self, storage=None):
        if not storage:
            self.sessions = DatabaseStorage()
        else:
            self.sessions = storage

    def get_session(self, session_id):
        session_data = self.sessions.get(session_id, None)
        if session_data == None:
            self.sessions[session_id] = Session(self, {'created_at': time.time(), 'content': {}})
            return {}
        return Session(self, session_data) #

    def delete_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def update_session(self, session_id, content):
        if session_id in self.sessions:
            self.sessions[session_id]['content'] = content
            return True
        return False

class Session(dict):
    def __init__(self, session_manager, initial_data=None):
        if initial_data is None:
            initial_data = {}
        self.session_manager = session_manager
        super(Session, self).__init__(initial_data)

    def __getitem__(self, key):
        if key not in self:
            raise KeyError(f"Key '{key}' not found in session.")
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        print(f"Setting key '{key}' to value '{value}' in session.")
        super().__setitem__(key, value)

session_manager = SessionManager()