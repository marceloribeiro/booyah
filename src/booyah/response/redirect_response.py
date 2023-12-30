from booyah.logger import logger
from booyah.session.session_manager import session_manager

class RedirectResponse:
    DEFAULT_HTTP_STATUS = '303 See Other'

    def __init__(self, environment, redirect_to):
        self.environment = environment
        self.status = self.DEFAULT_HTTP_STATUS
        self.redirect_to = redirect_to

    def response_headers(self):
        session_manager.save_session()
        full_path = self.redirect_to
        if 'HTTP_ORIGIN' in self.environment:
            full_path = self.environment['HTTP_ORIGIN'] + self.redirect_to
        logger.debug('REDIRECT:', full_path)
        return [
            ('Location', full_path),
        ]

    def format(self):
        return self.environment.get('RESPONSE_FORMAT')

    def response_body(self):
        return bytes()