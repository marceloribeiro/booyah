import re
from booyah.validators.application_validator import ApplicationValidator

class FormatValidator(ApplicationValidator):
    def validate(self):
        value = getattr(self.model, self.attribute)
        if not value or not re.match(self.validation_value, value):
            self.model.errors.append({ self.attribute: 'format is invalid' })