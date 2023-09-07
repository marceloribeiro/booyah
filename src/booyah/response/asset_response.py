import os

class AssetResponse:
    DEFAULT_HTTP_STATUS = '200 OK'

    def __init__(self, environment, status = DEFAULT_HTTP_STATUS):
        self.environment = environment
        self.file_name = os.path.join(os.environ["ROOT_PROJECT_PATH"], 'app', environment['PATH_INFO'][1:])
        self.load_file_content()
        self.status = status

    def response_headers(self):
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

    def response_body(self):
        return self.file_bytes
    
    def load_file_content(self):
        try:
            with open(self.file_name, 'rb') as file:
                self.file_bytes = file.read()
        except FileNotFoundError:
            self.status = "404 Not Found"
            print(f"File '{file_path}' not found.")
        except Exception as e:
            self.status = "500 Internal Server Error"
            print(f"An error occurred: {str(e)}")