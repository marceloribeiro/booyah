import os
import uuid

class S3Storage:
    def __init__(self, record, attachment, options):
        self.attachment = attachment
        self.bucket_name = options['bucket']
        self.s3 = record._s3_instance(attachment)
    
    def delete_file(self, file_name):
        file_path = self.attachment_folder() + file_name
        try:
            self.s3.Bucket(self.bucket_name).Object(file_name).delete()
            print(f"'{file_path}' has been successfully deleted.")
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                print(f"File '{file_path}' not found.")
            else:
                print(f"An error occurred: {e}")
    
    def attachment_folder(self, full_path=True):
        return f'https://{self.bucket_name}.s3.amazonaws.com/'
    
    def url(self, file_name):
        s3_object = self.s3.Object(self.bucket_name, file_name)
        result = s3_object.meta.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': file_name},
            ExpiresIn=3600  # Specify the expiration time in seconds
        )
        print('generated url: ' + result)
        return result

    def save(self, file_value):
        random_filename = str(uuid.uuid4())
        extension = str(file_value).split('.')[-1]
        full_file_name = f"{random_filename}.{extension}"
        self.s3.Bucket(self.bucket_name).upload_file(str(file_value), full_file_name)
        return full_file_name