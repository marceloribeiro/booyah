import re
from booyah.validators.application_validator import ApplicationValidator

class ComparisonValidator(ApplicationValidator):
    def validate(self):
        model_value = getattr(self.model, self.attribute)
        for key in self.validation_value.keys():
            comparison_value = self.validation_value[key]
            if key == 'greater_than':
                if model_value <= comparison_value:
                    self.model.errors.append({ self.attribute: 'must be greater than ' + str(comparison_value) })
            elif key == 'less_than':
                if model_value >= comparison_value:
                    self.model.errors.append({ self.attribute: 'must be less than ' + str(comparison_value) })
            elif key == 'greater_than_or_equal_to':
                if model_value < comparison_value:
                    self.model.errors.append({ self.attribute: 'must be greater than or equal to ' + str(comparison_value) })
            elif key == 'less_than_or_equal_to':
                if model_value > comparison_value:
                    self.model.errors.append({ self.attribute: 'must be less than or equal to ' + str(comparison_value) })
            elif key == 'equal_to':
                if model_value != comparison_value:
                    self.model.errors.append({ self.attribute: 'must be equal to ' + str(comparison_value) })
            elif key == 'not_equal_to':
                if model_value == comparison_value:
                    self.model.errors.append({ self.attribute: 'must not be equal to ' + str(comparison_value) })