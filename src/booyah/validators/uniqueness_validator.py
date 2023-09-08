from booyah.validators.application_validator import ApplicationValidator

class UniquenessValidator(ApplicationValidator):
    def validate(self):
        value = getattr(self.model, self.attribute)
        if self.validation_value == True:
            if self.model.exists({ self.attribute: value }):
                self.model.errors.append({ self.attribute: 'must be unique' })