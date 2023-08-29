import json
from booyah.logger import logger

class RedirectResponse:
    APP_NAME = 'booyah'
    DEFAULT_RESPONSE_ENCODING = 'utf-8'
    DEFAULT_HTTP_STATUS = '302 Found'
    DEFAULT_CONTENT_TYPE = 'text/html; charset=utf-8'

    def __init__(self, environment, redirect_to):
        self.environment = environment
        self.status = self.DEFAULT_HTTP_STATUS
        self.redirect_to = redirect_to

    def response_headers(self):
        full_path = self.environment['HTTP_ORIGIN'] + self.redirect_to
        logger.debug('REDIRECT:', full_path)
        return [
            ('Location', full_path),
        ]

    def format(self):
        return self.environment.get('RESPONSE_FORMAT')

    def response_body(self):
        return bytes()