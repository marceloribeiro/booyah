
import json
from booyah.models.session_storage import SessionStorage

class DatabaseStorage(dict):

    def find_record(self, key):
        if self.record and self.record.session_id != key:
            self.save()
            self.clear()
            self.record = None
        elif not self.record:
            self.record = SessionStorage.where('session_id', key)
            if self.record:
                self.record = self.record[0]
                self.clear()
                self.update(json.loads(self.record.data))
        return self.record

    def __getitem__(self, key):
        self.find_record(key)
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        self.find_record(key)
        super().__setitem__(key, value)
    
    def save(self, key):
        self.find_record(key)
        data = json.dumps(self)
        if self.record:
            self.record.data = data
        else:
            self.record = SessionStorage({'session_id': key, 'data': data})
        self.record.save()
