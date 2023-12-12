from booyah.models.application_model import ApplicationModel

class SessionStorage(ApplicationModel):
    @classmethod
    def table_name(self):
        return "session_storage"