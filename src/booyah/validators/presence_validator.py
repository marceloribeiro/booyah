from booyah.validators.application_validator import ApplicationValidator

class PresenceValidator(ApplicationValidator):
    def validate(self):
        value = getattr(self.model, self.attribute)
        if self.validation_value == True:
            if not value or value == None:
                self.model.errors.append({ self.attribute: 'must be present' })