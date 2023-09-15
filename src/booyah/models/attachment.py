import types
import boto3
from botocore.exceptions import NoCredentialsError
import os
from booyah.models.helpers.attachment_helper import save_attachments, validate_attachments, attachment_folder, delete_file
    
class Attachment:
    @staticmethod
    def configure(cls, name, required=False, bucket="booyah"):
        if not hasattr(cls, '_attachments'):
            cls._attachments = [name]
        else:
            cls._attachments.append(name)
        setattr(cls, name, None)
        setattr(cls, f"_{name}_options", {
            'required': required,
            'bucket': bucket
        })
        Attachment.copy_required_methods_to_class(cls)
        cls.custom_validates.append(cls.validate_attachments)

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
