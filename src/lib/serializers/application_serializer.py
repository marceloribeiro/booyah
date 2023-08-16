class ApplicationSerializer:
    def __init__(self, model):
        self.model = model

    def to_dict(self):
        return self.model.to_dict()

    def to_json(self):
        return self.model.to_json()