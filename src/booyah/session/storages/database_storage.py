
import json
from booyah.models.session_storage import SessionStorage
from booyah.session.storages.base_storage import BaseStorage

class DatabaseStorage(BaseStorage):
    def __init__(self):
        self.record = None

    def find_record(self, session_id):
        if self.record and self.record.session_id != session_id:
            self.record = None
        
        if not self.record:
            self.record = SessionStorage.where('session_id', session_id)
            if len(self.record) > 0:
                self.record = self.record[0]
                if self.record.is_expired():
                    self.record.destroy()
                    self.record = None
            else:
                self.record = None

    def get_session_dict(self, session_id):
        self.find_record(session_id)
        if self.record:
            return json.loads(self.record.data)
        else:
            return {}

    def destroy_session(self, session_id):
        self.find_record(session_id)
        if self.record:
            self.record.destroy()

    def save_session(self, session_id, data, expiration):
        self.find_record(session_id)
        data_str = json.dumps(data)
        if self.record:
            self.record.data = data_str
        else:
            self.record = SessionStorage({'session_id': session_id, 'data': data_str, 'expires_at': expiration})
        self.record.save()