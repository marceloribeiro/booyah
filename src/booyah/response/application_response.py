import json
import os
from jinja2 import Environment, PackageLoader, select_autoescape
from booyah.logger import logger
from booyah.cookies.cookies_manager import cookies_manager
from booyah.session.session_manager import session_manager

class ApplicationResponse:
    APP_NAME = 'booyah'
    DEFAULT_RESPONSE_ENCODING = 'utf-8'
    DEFAULT_HTTP_STATUS = '200 OK'
    DEFAULT_CONTENT_TYPE = 'text/html; charset=utf-8'

    def __init__(self, environment, data = {}, headers = [], status = DEFAULT_HTTP_STATUS):
        self.environment = environment
        self.data = data
        self.body = ''
        self.headers = headers
        self.status = status

        self.template_environment = Environment(
            loader=PackageLoader('booyah', 'templates') if os.getenv('BOOYAH_ENV') == 'test' else PackageLoader('app', 'views'),
            autoescape=select_autoescape()
        )

    def response_headers(self):
        session_manager.save_session()
        if (self.headers != []):
            return cookies_manager.apply_cookies(self.headers)
        else:
            default_headers = [
              ('Content-type', self.environment.get('CONTENT_TYPE', self.DEFAULT_CONTENT_TYPE)),
              ('Content-Length', str(len(self.body)))
            ]
            cookies_manager.apply_cookies(default_headers)
            return default_headers

    def format(self):
        return self.environment.get('RESPONSE_FORMAT')

    def response_body(self):
        format = self.format()
        if format:
            return getattr(self, format + '_body')()
        else:
            self.body = self.data
            return bytes(self.data, self.DEFAULT_RESPONSE_ENCODING)

    def text_body(self):
        self.body = self.data['text']
        return bytes(self.body, self.DEFAULT_RESPONSE_ENCODING)

    def html_body(self):
        template = self.template_environment.get_template(self.get_template_path())
        self.data['project_name'] = os.environ["PROJECT_NAME"]
        self.body = template.render(**self.data)
        return bytes(self.body, self.DEFAULT_RESPONSE_ENCODING)

    def json_body(self):
        self.body = json.dumps(self.data)
        return bytes(self.body, self.DEFAULT_RESPONSE_ENCODING)

    def get_template_path(self):
        template_path = f"{self.environment['controller_name']}/{self.environment['action_name']}.html"
        logger.debug("http accept:", self.environment['HTTP_ACCEPT'])
        logger.debug("rendering:", template_path, ', format:', self.format())
        return template_path