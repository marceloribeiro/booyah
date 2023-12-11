import os
import uuid

class LocalStorage:
    def __init__(self, record, attachment, options):
        self.attachment = attachment
        self.options = options
    
    def delete_file(self, file_name):
        file_path = os.path.join(self.attachment_folder(), file_name)
        try:
            os.remove(file_path)
            print(f"'{file_path}' has been successfully deleted.")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def attachment_folder(self, full_path=True):
        if full_path:
            return os.path.join(os.environ["ROOT_PROJECT_PATH"], 'public', 'attachments', self.options['bucket'])
        else:
            return '/' + os.path.join('attachments', self.options['bucket'])
    
    def url(self, file_name):
        folder_path = self.attachment_folder(full_path=False)
        return os.path.join(folder_path, file_name)

    def save(self, file_value):
        random_filename = str(uuid.uuid4())
        extension = str(file_value).split('.')[-1]
        full_file_name = f"{random_filename}.{extension}"
        destination_path = os.path.join(self.attachment_folder(), full_file_name)
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        os.rename(str(file_value), destination_path)
        return full_file_name