from booyah.controllers.application_controller import ApplicationController
import io

class HomeController(ApplicationController):
    def index(self):
        return self.render({'text': 'Home Controller, Index Action'})

class TestApplicationController:
    def setup_method(self):
        self._http_method = 'GET'
        self._query_string = ''
        self._wsgi_input = None
        self._matching_route = '/'
        self._matching_route_params = []
        self._content_length = 0


    def http_method(self):
        return self._http_method

    def query_string(self):
        return self._query_string

    def wsgi_input(self):
        return self._wsgi_input

    def matching_route(self):
        return self._matching_route

    def matching_route_params(self):
        return self._matching_route_params

    def environment(self):
        return {
          'REQUEST_METHOD': self.http_method(),
          'QUERY_STRING': self.query_string(),
          'CONTENT_LENGTH': self._content_length,
          'CONTENT_TYPE': 'application/json',
          'wsgi.input': self.wsgi_input(),
          'MATCHING_ROUTE': self.matching_route(),
          'MATCHING_ROUTE_PARAMS': self.matching_route_params(),
          'controller_name': 'home',
          'action_name': 'index',
          'HTTP_ACCEPT': 'text/html'
        }

    def test_is_get_request(self):
        self._http_method = 'GET'
        self.application_controller = ApplicationController(self.environment())
        assert self.application_controller.is_get_request() == True

    def test_is_post_request(self):
        self._http_method = 'POST'
        self.application_controller = ApplicationController(self.environment())
        assert self.application_controller.is_post_request() == True

    def test_is_put_request(self):
        self._http_method = 'PUT'
        self.application_controller = ApplicationController(self.environment())
        assert self.application_controller.is_put_request() == True

    def test_is_delete_request(self):
        self._http_method = 'DELETE'
        self.application_controller = ApplicationController(self.environment())
        assert self.application_controller.is_delete_request() == True

    def test_is_patch_request(self):
        self._http_method = 'PATCH'
        self.application_controller = ApplicationController(self.environment())
        assert self.application_controller.is_patch_request() == True

    def test_load_params_from_route(self):
        self._http_method = 'GET'
        self._matching_route = '/users/{id}'
        self._matching_route_params = ['1']
        self.application_controller = ApplicationController(self.environment())
        self.application_controller.load_params_from_route()
        assert self.application_controller.params == {'id': '1'}

    def test_load_params_from_query_string(self):
        self._http_method = 'GET'
        self._query_string = 'foo=bar'
        self.application_controller = ApplicationController(self.environment())
        self.application_controller.load_params_from_query_string()
        assert self.application_controller.params == {'foo': 'bar'}

    def test_load_params_from_gunicorn_body(self):
        self._http_method = 'POST'
        self._content_length = 14
        self._wsgi_input = io.StringIO('{"one": "two"}')
        self.application_controller = ApplicationController(self.environment())
        self.application_controller.load_params_from_gunicorn_body()
        assert self.application_controller.params == {'one': 'two'}

    def test_load_params(self):
        self._http_method = 'POST'
        self._content_length = 14
        self._matching_route = '/users/{id}'
        self._matching_route_params = ['1']
        self._query_string = 'foo=bar'
        self._wsgi_input = io.StringIO('{"one": "two"}')
        self.application_controller = ApplicationController(self.environment())
        self.application_controller.load_params()
        assert self.application_controller.params == {'id': '1', 'foo': 'bar', 'one': 'two'}

    def test_render(self):
        self.application_controller = ApplicationController(self.environment())
        assert self.application_controller.render({'foo': 'bar'}).json_body() == b'{"foo": "bar"}'

    def test_render_text(self):
        self.application_controller = ApplicationController(self.environment())
        assert self.application_controller.render({'text': 'foo'}).text_body() == b'foo'

    def test_render_html(self):
        self.application_controller = ApplicationController(self.environment())
        assert self.application_controller.render({'text': 'foo'}).html_body() == b'<h1>Index for Home</h1>\n<p>foo</p>'

    def test_render_json(self):
        self.application_controller = ApplicationController(self.environment())
        assert self.application_controller.render({'foo': 'bar'}).json_body() == b'{"foo": "bar"}'

    def test_get_action(self):
        self.home_controller = HomeController(self.environment())
        controller_action = self.home_controller.get_action('index')
        assert controller_action == self.home_controller.index