from booyah.response.application_response import ApplicationResponse
from booyah.cookies.cookies_manager import cookies_manager
from booyah.session.session_manager import session_manager
from booyah.models.session_storage import SessionStorage

class TestApplicationResponse:
    def content_type(self):
        return self._content_type

    def setup_method(self):
        self._content_type = 'application/json'
        self._environment = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/test',
            'QUERY_STRING': 'test=1',
            'CONTENT_TYPE': self.content_type(),
            'CONTENT_LENGTH': '0',
            'RESPONSE_FORMAT': 'json',
            'HTTP_ACCEPT': self.content_type(),
            'controller_name': 'home',
            'action_name': 'index'
        }
        self._data = { 'status': 'ok', 'text': 'hello world' }
        self.response = ApplicationResponse(self._environment, self._data)
        cookies_manager.initialize({})
        cookies_manager.create_session()
        session_manager.from_cookie()

    def test_response_headers(self):
        response_headers = self.response.response_headers()
        assert response_headers == [
            ('Content-type', self._environment.get('CONTENT_TYPE', '')),
            ('Content-Length', str(len(self.response.body))),
            ('Set-Cookie', response_headers[-2][1]),
            ('Set-Cookie', response_headers[-1][1])
        ]

    def test_format(self):
        assert self.response.format() == 'json'

    def test_response_body(self):
        self._environment['RESPONSE_FORMAT'] = 'json'
        assert self.response.response_body() == b'{"status": "ok", "text": "hello world"}'
        self._environment['RESPONSE_FORMAT'] = 'html'
        assert self.response.response_body() == b'<h1>Index for Home</h1>\n<p>hello world</p>'
        self._environment['RESPONSE_FORMAT'] = 'text'
        assert self.response.response_body() == b'hello world'

    def test_text_body(self):
        assert self.response.text_body() == b'hello world'

    def test_html_body(self):
        assert self.response.html_body() == b'<h1>Index for Home</h1>\n<p>hello world</p>'

    def test_json_body(self):
        assert self.response.json_body() == b'{"status": "ok", "text": "hello world"}'

    def test_get_template_path(self):
        assert self.response.get_template_path() == 'home/index.html'