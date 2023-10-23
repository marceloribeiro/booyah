from booyah.models.booyah_attachment import BooyahAttachment
from booyah.models.application_model import ApplicationModel

class CustomModel(ApplicationModel):
    pass
BooyahAttachment.configure(CustomModel, 'photo', required=False)

class TestAttachment:
    def create_custom_models_table(self):
        CustomModel.drop_table()
        CustomModel.create_table({
            'id': 'primary_key',
            'name': 'string',
            'photo': 'string',
            'created_at': 'datetime',
            'updated_at': 'datetime'
        })

    def create_custom_model(self, name='Test User', email='test@email.com'):
        CustomModel.create({
            'name': name,
            'email': email,
        })

    def create_custom_model_sample(self):
        self.create_custom_models_table()
        self.create_custom_model()
        self.create_custom_model(name='Another', email='another@email.com')
        self.create_custom_model(name='Third', email='third@email.com')
    
    def test_configure(self):
        self.create_custom_model_sample()
        CustomModel.find(1)
        ApplicationModel._custom_validates = False
        assert CustomModel._photo_options['required'] == False
        assert CustomModel._custom_validates == []
        assert hasattr(CustomModel, '_custom_validates') == True
        assert CustomModel._custom_validates == []
        assert hasattr(ApplicationModel, '_custom_validates') != CustomModel._custom_validates
        assert hasattr(CustomModel, '_validate_attachments') and callable(getattr(CustomModel, '_validate_attachments')) == True
        assert hasattr(ApplicationModel, 'validate_attachments')  == False
