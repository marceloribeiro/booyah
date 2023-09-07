import os
from booyah.logger import logger

class AssetResponse:
    APP_NAME = 'booyah'
    DEFAULT_RESPONSE_ENCODING = 'utf-8'
    DEFAULT_HTTP_STATUS = '200 OK'

    def __init__(self, environment, headers = [], status = DEFAULT_HTTP_STATUS):
        self.environment = environment
        self.file_name = os.path.join(os.environ["ROOT_PROJECT_PATH"], 'app', environment['PATH_INFO'][1:])
        self.load_file_content()
        self.headers = headers
        self.status = status

    def response_headers(self):
        if (self.headers != []):
            return self.headers
        else:
            return [
              ('Content-type', self.environment.get('CONTENT_TYPE', self.get_content_type())),
              ('Content-Length', str(len(self.file_bytes)))
            ]
    
    def get_content_type(self):
        file_extension = self.file_name.lower()

        if file_extension.endswith('.html'):
            return 'text/html'
        elif file_extension.endswith('.htm'):
            return 'text/html'
        elif file_extension.endswith('.css'):
            return 'text/css'
        elif file_extension.endswith('.js'):
            return 'text/javascript'
        elif file_extension.endswith('.json'):
            return 'application/json'
        elif file_extension.endswith('.ico'):
            return 'image/x-icon'
        elif file_extension.endswith('.pdf'):
            return 'application/pdf'
        elif file_extension.endswith('.png'):
            return 'image/png'
        elif file_extension.endswith('.jpg') or file_extension.endswith('.jpeg'):
            return 'image/jpeg'
        elif file_extension.endswith('.gif'):
            return 'image/gif'
        elif file_extension.endswith('.svg'):
            return 'image/svg+xml'
        elif file_extension.endswith('.xml'):
            return 'application/xml'
        elif file_extension.endswith('.txt'):
            return 'text/plain'
        elif file_extension.endswith('.zip'):
            return 'application/zip'
        else:
            return 'application/octet-stream' 

    def format(self):
        return self.environment.get('RESPONSE_FORMAT')

    def response_body(self):
        return self.file_bytes
    
    def load_file_content(self):
        try:
            with open(self.file_name, 'rb') as file:
                self.file_bytes = file.read()
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")