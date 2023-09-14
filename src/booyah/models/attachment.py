import types
import boto3
from botocore.exceptions import NoCredentialsError
from booyah.models.file import File
import os
import uuid

class Attachment:
    @staticmethod
    def configure(cls, name, required=False):
        if not hasattr(cls, '_attachments'):
            cls._attachments = [name]
        else:
            cls._attachments.append(name)
        setattr(cls, name, None)
        setattr(cls, f"_{name}_options", {
            'required': required
        })
        Attachment.copy_required_methods_to_class(cls)

    @staticmethod
    def copy_required_methods_to_class(cls):
        cls.validate_attachments = Attachment.validate_attachments.__get__(cls)
        cls.bucket_name = Attachment.bucket_name.__get__(cls)
        cls.save_attachments = Attachment.save_attachments.__get__(cls)
        cls.save_local_attachment = Attachment.save_local_attachment.__get__(cls)
    
    @classmethod
    def bucket_name(self):
        return 'booyah'
    
    @classmethod
    def validate_attachments(self):
        has_error = False
        for attachment in self._attachments:
            options = getattr(self, f"_{attachment}_options")
            if options['required'] and not getattr(self, attachment):
                print(f'{attachment} should not be blank.')
                has_error = True
            else:
                print(f'{attachment} is valid')
        return not has_error

    @classmethod
    def save_attachments(self, attributes = None):
        # delete_file_from_s3('your-s3-bucket-name', s3_key)
        # get_file_from_s3('your-s3-bucket-name', s3_key)
        # upload_file_to_s3(file, 'your-s3-bucket-name', 'uploads/file.jpg')
        if not attributes:
            return attributes

        for attachment in self._attachments:
            options = getattr(self, f"_{attachment}_options")
            current_value = attributes[attachment]
            if type(current_value) is File:
                random_filename = str(uuid.uuid4())
                extension = str(current_value).split('.')[-1]
                full_file_name = f"{random_filename}.{extension}"

                if os.getenv('BOOYAH_ENV') != 'production':
                    target_path = os.path.join(os.environ["ROOT_PROJECT_PATH"], 'public', 'files', self.bucket_name(), full_file_name)
                    self.save_local_attachment(str(current_value), target_path)
                    attributes[attachment] = full_file_name
        return attributes

    def save_local_attachment(self, source_path, destination_path):
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        os.rename(source_path, destination_path)


    def upload_file_to_s3(self, file, bucket_name, object_name):
        s3 = boto3.client('s3')
        try:
            s3.upload_fileobj(file, bucket_name, object_name)
            return True
        except FileNotFoundError:
            return False
        except NoCredentialsError:
            return False

    def get_file_from_s3(self, bucket_name, object_name):
        s3 = boto3.client('s3')
        try:
            response = s3.get_object(Bucket=bucket_name, Key=object_name)
            return response['Body'].read()
        except NoCredentialsError:
            return None
    
    def delete_file_from_s3(self, bucket_name, object_name):
        s3 = boto3.client('s3')
        try:
            s3.delete_object(Bucket=bucket_name, Key=object_name)
            return True
        except NoCredentialsError:
            return False