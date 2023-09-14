import json
from booyah.response.application_response import ApplicationResponse
from booyah.response.redirect_response import RedirectResponse
from urllib.parse import parse_qs
from booyah.logger import logger
from booyah.helpers.request_format_helper import RequestFormatHelper, ContentType
from booyah.application_support.action_support import ActionSupport
import cgi
import tempfile
from booyah.models.file import File
import os

class BooyahApplicationController(ActionSupport):
    def __init__(self, environment, should_load_params=True):
        self.environment = environment
        self.params = {}
        self.application_response = None
        if should_load_params:
            self.load_params()

    def respond_to(self, html=None, json=None, text=None):
        return RequestFormatHelper(self.environment).respond_to(html, json, text)

    def load_params(self):
        self.load_params_from_route()
        self.load_params_from_query_string()
        self.load_params_from_gunicorn_body()
        logger.debug("PARAMS:", self.params)

    def load_params_from_route(self):
        if 'MATCHING_ROUTE_PARAMS' in self.environment:
            self.params.update(self.environment['MATCHING_ROUTE_PARAMS'])

    def load_params_from_query_string(self):
        query_string = None
        if 'QUERY_STRING' in self.environment:
            query_string = self.environment['QUERY_STRING']

        params = {}
        if query_string:
            for param in query_string.split('&'):
                key, value = param.split('=')
                params[key] = value
        self.params.update(params)

    def parse_nested_attributes(self, body_data):
        parsed_data = parse_qs(body_data)
        nested_data = {}
        for key, value in parsed_data.items():
            keys = key.split("[")
            current_dict = nested_data
            for k in keys[:-1]:
                current_dict = current_dict.setdefault(k, {})

            if len(keys) == 1:
                current_dict[keys[-1]] = value[0]
            else:
                current_dict[keys[-1][:-1]] = value[0]

        return nested_data

    def load_params_from_gunicorn_body(self):
        if self.environment.get('CONTENT_LENGTH') is None or 'CONTENT_TYPE' not in self.environment:
            return

        content_type = self.environment['CONTENT_TYPE']
        content_length = int(self.environment['CONTENT_LENGTH'])
        body_params = {}
        if content_length:
            body = self.environment['wsgi.input'].read(content_length)
            if content_type == ContentType.JSON.value:
                try:
                    body_json = body.decode('utf-8')
                except:
                    body_json = body
                body_params = json.loads(body_json)
            elif content_type == ContentType.FORM_URLENCODED.value:
                body_params = self.parse_nested_attributes(str(body.decode('utf-8')))
            elif ContentType.MULTIPART.value in content_type:
                body_params = self.parse_multipart(body)
            else:
                for param in body.decode('utf-8').split('&'):
                    key, value = param.split('=')
                    body_params[key] = value
        self.params.update(body_params)
    
    def flatten_dict(self, d):
        result = {}
        for key, value in d.items():
            parts = key.split('[')
            current = result
            for part in parts[:-1]:
                part = part.strip(']')
                current = current.setdefault(part, {})
            current[parts[-1].strip(']')] = value
        return result
    
    def parse_multipart(self, body_bytes, temp_dir=None):
        content_type = self.environment['CONTENT_TYPE']
        _, params = cgi.parse_header(content_type)
        boundary = params.get('boundary')

        parts = []
        if not boundary:
            boundary = body_bytes.split(b"\r\n")[0][2:]
        else:
            boundary = boundary.encode()
        parts = body_bytes.split(b'--' + boundary)
        form_data = {}

        for part in parts[1:-1]:
            headers, content = part.split(b'\r\n\r\n', 1)
            field_data = cgi.parse_header(headers.decode())
            field_name = field_data[1].get('name')

            if field_name:
                if 'filename' in field_data[1]:
                    filename = field_data[1]['filename'].split('\r\n')[0].replace("\"", "")
                    file_extension = os.path.splitext(filename)[-1]
                    temp_file = tempfile.NamedTemporaryFile(delete=False, dir=temp_dir, suffix=file_extension)
                    temp_file.write(content)
                    temp_file.close()
                    form_data[field_name] = File(temp_file.name)
                else:
                    form_data[field_name] = content.rstrip(b'\r\n').decode()

        form_data = self.flatten_dict(form_data)
        return form_data

    def render(self, data = {}):
        self.application_response = ApplicationResponse(self.environment, data)
        return self.application_response

    def redirect(self, redirect_to):
        return RedirectResponse(self.environment, redirect_to)

    def is_get_request(self):
        return self.environment['REQUEST_METHOD'] == 'GET'

    def is_post_request(self):
        return self.environment['REQUEST_METHOD'] == 'POST'

    def is_put_request(self):
        return self.environment['REQUEST_METHOD'] == 'PUT'

    def is_delete_request(self):
        return self.environment['REQUEST_METHOD'] == 'DELETE'

    def is_patch_request(self):
        return self.environment['REQUEST_METHOD'] == 'PATCH'