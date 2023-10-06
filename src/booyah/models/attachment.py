import types
import boto3
from botocore.exceptions import NoCredentialsError
import os
from booyah.models.helpers.attachment_helper import save_attachments, validate_attachments, attachment_folder, delete_file, add_field_method
from booyah.observers.application_model_observer import ApplicationModelObserver

class Attachment:
    @staticmethod
    def configure(cls, name, required=False, bucket="booyah", content_types=[]):
        if not hasattr(cls, '_attachments'):
            cls._attachments = [name]
        else:
            cls._attachments.append(name)
        setattr(cls, f"_{name}_options", {
            'required': required,
            'bucket': bucket,
            'content_types': content_types
        })
        Attachment.copy_required_methods_to_class(cls)
        Attachment.add_methods(cls, name)
        if not hasattr(cls, 'custom_validates'):
            cls.custom_validates = []
        cls.custom_validates.append(cls.validate_attachments)
        ApplicationModelObserver.add_callback('before_save', cls.__name__, 'save_attachments')

    @staticmethod
    def copy_required_methods_to_class(cls):
        cls.validate_attachments = validate_attachments
        cls.save_attachments = save_attachments
        cls.save_local_attachment = Attachment.save_local_attachment.__get__(cls)
        cls.delete_file = delete_file
        cls.attachment_folder = attachment_folder

    def save_local_attachment(self, source_path, destination_path):
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        os.rename(source_path, destination_path)
    
    @staticmethod
    def add_methods(cls, name):
        add_field_method(cls, name)