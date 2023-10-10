from booyah.models.attachment import Attachment
from booyah.models.file import File
from booyah.models.application_model import ApplicationModel
from booyah.models.helpers.attachment_helper import *
import tempfile

class CustomModel(ApplicationModel):
    pass
Attachment.configure(CustomModel, 'photo', required=False, bucket='test_files')

class TestAttachmentHelper:
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
    
    def test_save_attachments(self):
        self.create_custom_model_sample()
        custom_record = CustomModel.find(1)
        temp_file_path = None
        content = "This is the content of the temporary file."
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt") as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        custom_record.photo = File(temp_file_path, "original.txt")
        custom_record._save_attachments()
        expected_destination = os.path.abspath(f'tests/public/attachments/test_files/{custom_record.photo}')
        assert os.path.exists(expected_destination) == True
        with open(expected_destination, 'r') as file:
            file_content = file.read()
        assert file_content == content

    def test_validate_attachments(self):
        self.create_custom_model_sample()
        custom_record = CustomModel.find(1)
        CustomModel._photo_options = {"required": True, "bucket": CustomModel._photo_options["bucket"]}
        custom_record._validate_attachments()
        CustomModel._photo_options = {"required": False, "bucket": CustomModel._photo_options["bucket"]}
        assert custom_record.errors == ['photo should not be blank.']
    
    def test_should_automatically_delete_previous_file(self):
        self.create_custom_model_sample()
        custom_record = CustomModel()
        first_file_path = None
        content = "This is the content of the temporary file."
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt") as temp_file:
            temp_file.write(content)
            first_file_path = temp_file.name
        custom_record.photo = File(first_file_path, "original.txt")
        custom_record._save_attachments()
        first_expected_destination = os.path.abspath(f'tests/public/attachments/test_files/{custom_record.photo}')
        assert os.path.exists(first_expected_destination) == True
        custom_record.photo_was = custom_record.photo

        second_file_path = None
        second_content = "Content of the second file"
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt") as temp_file:
            temp_file.write(second_content)
            second_file_path = temp_file.name
        custom_record.photo = File(second_file_path, "second.txt")
        custom_record._save_attachments()
        second_expected_destination = os.path.abspath(f'tests/public/attachments/test_files/{custom_record.photo}')
        assert os.path.exists(first_expected_destination) == False
        assert os.path.exists(second_expected_destination) == True
        with open(second_expected_destination, 'r') as file:
            file_content = file.read()
        assert file_content == second_content