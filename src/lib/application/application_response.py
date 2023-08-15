import json
from jinja2 import Environment, PackageLoader, select_autoescape

class ApplicationResponse:
    APP_NAME = 'booyah'
    DEFAULT_RESPONSE_ENCODING = 'utf-8'
    RESPONSE_FORMAT_HTML = 'html'
    RESPONSE_FORMAT_TEXT = 'text'
    RESPONSE_FORMAT_JSON = 'json'
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
              ('Content-type', self.get_content_type()),
              ('Content-Length', str(len(self.body)))
          ]

    def get_content_type(self):
        accepts = self.environment['HTTP_ACCEPT'].split(',')[0]
        return accepts

    def format(self):
        content_type = self.get_content_type()
        if (content_type == 'text/html'):
            return self.RESPONSE_FORMAT_HTML
        elif (content_type == 'application/json'):
            return self.RESPONSE_FORMAT_JSON
        elif (content_type == 'text/plain'):
            return self.RESPONSE_FORMAT_TEXT
        else:
            return self.RESPONSE_FORMAT_HTML

    def response_body(self):
        return getattr(self, self.format() + '_body')()

    def text_body(self):
        self.body = self.data
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
        print('DEBUG Rendering: ' + template_path)
        return template_path