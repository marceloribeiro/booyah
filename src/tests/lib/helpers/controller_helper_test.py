from booyah.helpers.controller_helper import *
from booyah.controllers.home_controller import HomeController

class TestControllerHelper():
    def setup_method(self):
        self.environment = { 'HTTP_ACCEPT': 'application/json' }

    def test_get_controller_action(self):
        assert get_controller_action({ 'controller': 'home', 'action': 'index' }, self.environment)().json_body() == b'{"text": "Home Controller, Index Action"}'
        assert get_controller_action({ 'to': 'home#index' }, self.environment)().json_body() == b'{"text": "Home Controller, Index Action"}'

    def test_set_response_format(self):
        assert(set_response_format({ 'format': 'json' }, self.environment) == 'json')
        assert(self.environment['RESPONSE_FORMAT'] == 'json')
        assert(self.environment['CONTENT_TYPE'] == 'application/json')

    def test_content_type_from_response_format(self):
        assert(content_type_from_response_format('json') == 'application/json')
        assert(content_type_from_response_format('html') == 'text/html')
        assert(content_type_from_response_format('text') == 'text/plain')
        assert(content_type_from_response_format('foo') == 'text/html')

    def test_get_format_from_content_type(self):
        assert(get_format_from_content_type('application/json') == 'json')
        assert(get_format_from_content_type('text/html') == 'html')
        assert(get_format_from_content_type('text/plain') == 'text')
        assert(get_format_from_content_type('foo') == 'html')
