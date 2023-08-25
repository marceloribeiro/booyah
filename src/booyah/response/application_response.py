import json
from jinja2 import Environment, PackageLoader, select_autoescape
from booyah.logger import logger

class ApplicationResponse:
    APP_NAME = 'booyah'
    DEFAULT_RESPONSE_ENCODING = 'utf-8'
    DEFAULT_HTTP_STATUS = '200 OK'

    def __init__(self, environment, data = {}, headers = {}, status = DEFAULT_HTTP_STATUS):
        self.environment = environment
        self.data = data
        self.body = ''
        self.headers = headers
        self.status = status
        self.template_environment = Environment(
            loader=PackageLoader(self.APP_NAME),
            autoescape=select_autoescape()
        )

    def response_headers(self):
        if (self.headers != {}):
            return self.headers
        else:
          return [
              ('Content-type', self.environment.get('CONTENT_TYPE', '')),
              ('Content-Length', str(len(self.body)))
          ]

    def format(self):
        return self.environment.get('RESPONSE_FORMAT')

    def response_body(self):
        format = self.format()
        if format:
            return getattr(self, format + '_body')()
        else:
            return bytes(self.data, self.DEFAULT_RESPONSE_ENCODING)

    def text_body(self):
        self.body = self.data['text']
        return bytes(self.body, self.DEFAULT_RESPONSE_ENCODING)

    def html_body(self):
        template = self.template_environment.get_template(self.get_template_path())
        self.body = template.render(**self.data)
        return bytes(self.body, self.DEFAULT_RESPONSE_ENCODING)

    def json_body(self):
        self.body = json.dumps(self.data)
        return bytes(self.body, self.DEFAULT_RESPONSE_ENCODING)

    def get_template_path(self):
        template_path = self.environment['controller_name'] + '/' + self.environment['action_name'] + '.html'
        logger.debug("http accept:", self.environment['HTTP_ACCEPT'])
        logger.debug("rendering:", template_path, ', format:', self.format())
        return template_path