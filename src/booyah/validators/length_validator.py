from booyah.validators.application_validator import ApplicationValidator

class LengthValidator(ApplicationValidator):
    def validate(self):
        model_value = getattr(self.model, self.attribute)
        for key in self.validation_value.keys():
            comparison_value = self.validation_value[key]
            if key == 'minimum':
                if len(model_value) < comparison_value:
                    self.model.errors.append({ self.attribute: 'must be at least ' + str(comparison_value) + ' characters' })
            elif key == 'maximum':
                if len(model_value) > comparison_value:
                    self.model.errors.append({ self.attribute: 'must be at most ' + str(comparison_value) + ' characters' })