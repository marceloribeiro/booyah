from booyah.models.attachment import Attachment
from booyah.models.application_model import ApplicationModel

class CustomModel(ApplicationModel):
    pass
Attachment.configure(CustomModel, 'photo', required=False)

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
        custom_record = CustomModel.find(1)
        assert CustomModel._photo_options['required'] == False
        assert CustomModel.custom_validates != []
        assert hasattr(CustomModel, 'custom_validates') == True
        assert CustomModel.custom_validates != []
        assert hasattr(ApplicationModel, 'custom_validates') == False
