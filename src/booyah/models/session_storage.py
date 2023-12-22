from booyah.models.application_model import ApplicationModel
from datetime import datetime

class SessionStorage(ApplicationModel):
    @classmethod
    def table_name(self):
        return "session_storage"
    
    def is_expired(self):
        if self.expires_at:
            return datetime.utcnow() > self.expires_at
        else:
            return False