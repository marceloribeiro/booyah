from enum import Enum
import re
import tempfile
from booyah.models.file import File
import os

class ContentType(Enum):
    JSON = "application/json"
    XML = "application/xml"
    FORM_URLENCODED = "application/x-www-form-urlencoded"
    TEXT = "text/plain"
    HTML = "text/html"
    MULTIPART = "multipart/form-data"

class RequestFormatHelper:
    def __init__(self, environment):
        self.environment = environment
        if 'HTTP_ACCEPT' in environment:
            self.http_accept = environment['HTTP_ACCEPT']
        else:
            raise ValueError("Missing http accept header")

    def respond_to(self, html_block=None, json_block=None, text_block=None):
        if html_block is not None and (ContentType.HTML.value in self.http_accept or self.http_accept == '*/*'):
            self.environment['CONTENT_TYPE'] = ContentType.HTML.value
            return html_block()
        if json_block is not None and (ContentType.JSON.value in self.http_accept or self.http_accept == '*/*'):
            self.environment['CONTENT_TYPE'] = ContentType.JSON.value
            return json_block()
        if text_block is not None and (ContentType.TEXT.value in self.http_accept or self.http_accept == '*/*'):
            self.environment['CONTENT_TYPE'] = ContentType.TEXT.value
            return text_block()

        # if not included in accept, will return prior argument
        if html_block is not None:
            self.environment['CONTENT_TYPE'] = ContentType.HTML.value
            return html_block()
        if json_block is not None:
            self.environment['CONTENT_TYPE'] = ContentType.JSON.value
            return json_block()
        if text_block is not None:
            self.environment['CONTENT_TYPE'] = ContentType.TEXT.value
            return text_block()

def parse_header(header):
    params = {}
    parts = header.split(";")
    main_value = parts[0].strip()
    for part in parts[1:]:
        key, value = part.split("=", 1)
        params[key.strip()] = value.strip(' "')
    return main_value, params

def flatten_dict(d):
    result = {}
    for key, value in d.items():
        parts = key.split('[')
        current = result
        for part in parts[:-1]:
            part = part.strip(']')
            current = current.setdefault(part, {})
        current[parts[-1].strip(']')] = value
    return result

def parse_multipart(environment, body_bytes, temp_dir=None):
    content_type = environment['CONTENT_TYPE']
    _, params = parse_header(content_type)
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
        content = content[:-2]
        field_data = parse_header(headers.decode())
        field_name = field_data[1].get('name')

        if field_name:
            if 'filename' in field_data[1]:
                filename = field_data[1]['filename'].split('\r\n')[0].replace("\"", "")
                if filename:
                    file_extension = os.path.splitext(filename)[-1]
                    temp_file = tempfile.NamedTemporaryFile(delete=False, dir=temp_dir, suffix=file_extension)
                    temp_file.write(content)
                    temp_file.close()
                    form_data[field_name] = File(temp_file.name, filename, os.path.getsize(temp_file.name), environment)
            else:
                form_data[field_name] = content.rstrip(b'\r\n').decode()
    form_data = flatten_dict(form_data)
    return form_data