from booyah.helpers.request_format_helper import *

HTML_RESPONSE = '<html></html>'
JSON_RESPONSE = '{"json": "json response"}'
TEXT_RESPONSE = 'text response'

def html_response():
    return HTML_RESPONSE

def json_response():
    return JSON_RESPONSE

def text_response():
    return TEXT_RESPONSE

class TestRequestFormatHelper():
    def setup_method(self):
        self._boundary = "boundaryidentifier"
        self._content_type = f"multipart/form-data; boundary={self._boundary}"
        self._environment = {
            'HTTP_ACCEPT': '',
            'CONTENT_TYPE': ''
        }

    def test_parse_header(self):
        parse_result = parse_header(self._content_type)
        assert parse_result == ('multipart/form-data', {'boundary': self._boundary})

    def test_parse_header_with_filename(self):
        self._content_type = f'Content-Disposition: form-data; name="user[photo]"; filename="photo.png"'
        parse_result = parse_header(self._content_type)
        assert parse_result == ('Content-Disposition: form-data', {'name': 'user[photo]', 'filename': 'photo.png'})

    def test_respond_html(self):
        self._environment['HTTP_ACCEPT'] = 'text/html'
        request = RequestFormatHelper(self._environment)
        assert request.respond_to(html=html_response, json=json_response, text=text_response) == HTML_RESPONSE
        assert self._environment['CONTENT_TYPE'] == 'text/html'

    def test_respond_json(self):
        self._environment['HTTP_ACCEPT'] = 'application/json'
        request = RequestFormatHelper(self._environment)
        assert request.respond_to(html=html_response, json=json_response, text=text_response) == JSON_RESPONSE
        assert self._environment['CONTENT_TYPE'] == 'application/json'

    def test_respond_text(self):
        self._environment['HTTP_ACCEPT'] = 'text/plain'
        request = RequestFormatHelper(self._environment)
        assert request.respond_to(html=html_response, json=json_response, text=text_response) == TEXT_RESPONSE
        assert self._environment['CONTENT_TYPE'] == 'text/plain'