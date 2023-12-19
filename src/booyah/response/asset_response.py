import os
from booyah.response.mime_types import MIME_TYPE_BY_EXTENSION, DEFAULT_MIME_TYPE
from booyah.framework import Booyah

class AssetResponse:
    DEFAULT_HTTP_STATUS = '200 OK'

    def __init__(self, environment, status = DEFAULT_HTTP_STATUS):
        self.environment = environment
        self.file_name = os.path.join(Booyah.root, 'app', environment['PATH_INFO'][1:])
        self.load_file_content()
        self.status = status

    def response_headers(self):
        return [
            ('Content-type', self.environment.get('CONTENT_TYPE', self.get_content_type())),
            ('Content-Length', str(len(self.file_bytes)))
        ]
    
    def get_content_type(self):
        _, file_extension = os.path.splitext(self.file_name.lower())
        if file_extension and file_extension[0] == '.':
            file_extension = file_extension[1:]
        return MIME_TYPE_BY_EXTENSION.get(file_extension, DEFAULT_MIME_TYPE)

    def response_body(self):
        return self.file_bytes
    
    def load_file_content(self):
        try:
            with open(self.file_name, 'rb') as file:
                self.file_bytes = file.read()
        except FileNotFoundError:
            self.status = "404 Not Found"
            self.file_bytes = b""
            print(f"File '{file_path}' not found.")
        except Exception as e:
            self.status = "500 Internal Server Error"
            self.file_bytes = b""
            print(f"An error occurred: {str(e)}")