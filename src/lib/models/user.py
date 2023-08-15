from lib.models.application_model import ApplicationModel

class User(ApplicationModel):
    def __init__(self, attributes = {}):
        self.attributes = attributes