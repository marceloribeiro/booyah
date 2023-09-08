class ApplicationValidator:
    def __init__(self, model, attribute, validation_value):
        self.model = model
        self.attribute = attribute
        self.validation_value = validation_value