from booyah.validators.application_validator import ApplicationValidator

class PresenceValidator(ApplicationValidator):
    def validate(self):
        value = getattr(self.model, self.attribute)
        if self.validation_value == True:
            if value == None or len(value) == 0:
                self.model.errors.append({ self.attribute: 'must be present' })