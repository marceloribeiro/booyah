from booyah.controllers.application_controller import BooyahApplicationController
import io
from booyah.models.file import File

class HomeController(BooyahApplicationController):
    def index(self):
        return self.render({'text': 'Home Controller, Index Action'})

class TestApplicationController:
    def setup_method(self):
        self._http_method = 'GET'
        self._query_string = ''
        self._wsgi_input = None
        self._matching_route = '/'
        self._matching_route_params = {}
        self._content_length = 0
        self._content_type = 'application/json'

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
          'CONTENT_TYPE': self._content_type,
          'wsgi.input': self.wsgi_input(),
          'MATCHING_ROUTE': self.matching_route(),
          'MATCHING_ROUTE_PARAMS': self.matching_route_params(),
          'controller_name': 'home',
          'action_name': 'index',
          'HTTP_ACCEPT': 'text/html'
        }

    def test_is_get_request(self):
        self._http_method = 'GET'
        self.application_controller = BooyahApplicationController(self.environment())
        assert self.application_controller.is_get_request() == True

    def test_is_post_request(self):
        self._http_method = 'POST'
        self.application_controller = BooyahApplicationController(self.environment())
        assert self.application_controller.is_post_request() == True

    def test_is_put_request(self):
        self._http_method = 'PUT'
        self.application_controller = BooyahApplicationController(self.environment())
        assert self.application_controller.is_put_request() == True

    def test_is_delete_request(self):
        self._http_method = 'DELETE'
        self.application_controller = BooyahApplicationController(self.environment())
        assert self.application_controller.is_delete_request() == True

    def test_is_patch_request(self):
        self._http_method = 'PATCH'
        self.application_controller = BooyahApplicationController(self.environment())
        assert self.application_controller.is_patch_request() == True

    def test_load_params_from_route(self):
        self._http_method = 'GET'
        self._matching_route = '/users/<int:id>'
        self._matching_route_params = {'id': 1}
        self.application_controller = BooyahApplicationController(self.environment())
        self.application_controller.load_params_from_route()
        assert self.application_controller.params == {'id': 1}

    def test_load_params_from_query_string(self):
        self._http_method = 'GET'
        self._query_string = 'foo=bar'
        self.application_controller = BooyahApplicationController(self.environment())
        self.application_controller.load_params_from_query_string()
        assert self.application_controller.params == {'foo': 'bar'}

    def test_load_params_from_gunicorn_body(self):
        self._http_method = 'POST'
        self._wsgi_input = io.StringIO('{"one": "two"}')
        self._content_length = 14
        self.application_controller = BooyahApplicationController(self.environment(), False)
        self.application_controller.load_params_from_gunicorn_body()
        assert self.application_controller.params == {'one': 'two'}

    def test_load_params(self):
        self._http_method = 'POST'
        self._content_length = 14
        self._matching_route = '/users/{id}'
        self._matching_route_params = {'id': 1}
        self._query_string = 'foo=bar'
        self._wsgi_input = io.StringIO('{"one": "two"}')
        self.application_controller = BooyahApplicationController(self.environment(), False)
        self.application_controller.load_params()
        assert self.application_controller.params == {'id': 1, 'foo': 'bar', 'one': 'two'}

    def test_parse_nested_attributes(self):
        self.application_controller = BooyahApplicationController(self.environment(), False)
        params = self.application_controller.parse_nested_attributes("user%5Bname%5D=Klaus&user%5Bemail%5D=my%40email.com&token=123")
        assert params == {'user': {'name': 'Klaus', 'email': 'my@email.com'}, 'token': '123'}

    def test_render(self):
        self.application_controller = BooyahApplicationController(self.environment())
        assert self.application_controller.render({'foo': 'bar'}).json_body() == b'{"foo": "bar"}'

    def test_render_text(self):
        self.application_controller = BooyahApplicationController(self.environment())
        assert self.application_controller.render({'text': 'foo'}).text_body() == b'foo'

    def test_render_html(self):
        self.application_controller = BooyahApplicationController(self.environment())
        assert self.application_controller.render({'text': 'foo'}).html_body() == b'<h1>Index for Home</h1>\n<p>foo</p>'

    def test_render_json(self):
        self.application_controller = BooyahApplicationController(self.environment())
        assert self.application_controller.render({'foo': 'bar'}).json_body() == b'{"foo": "bar"}'

    def test_get_action(self):
        self.home_controller = HomeController(self.environment())
        controller_action = self.home_controller.get_action('index')
        assert controller_action == self.home_controller.index
    
    def test_parse_multipart(self):
        boundary = "boundaryidentifier"
        self._content_type = f"multipart/form-data; boundary={boundary}"
        form_data = [
            ('user[name]', 'John'),
            ('user[email]', 'john@doe.com'),
        ]

        multipart_body = []

        for field_name, field_value in form_data:
            multipart_body.append(f'--{boundary}')
            multipart_body.append(f'Content-Disposition: form-data; name="{field_name}"')
            multipart_body.append('')
            multipart_body.append(field_value)

        file_field_name = "user[photo]"
        file_content = "This is the content of the file."

        multipart_body.append(f'--{boundary}')
        multipart_body.append(f'Content-Disposition: form-data; name="{file_field_name}"; filename="user_photo.png"')
        multipart_body.append('Content-Type: image/png')
        multipart_body.append('')
        multipart_body.append(file_content)

        multipart_body.append(f'--{boundary}--')
        multipart_body.append('')

        multipart_data = '\r\n'.join(multipart_body).encode('utf-8')

        application_controller = BooyahApplicationController(self.environment(), False)
        parsed_params = application_controller.parse_multipart(multipart_data)

        assert 'user' in parsed_params.keys()
        assert list(parsed_params['user'].keys()) == ['name', 'email', 'photo']
        assert parsed_params['user']['name'] == 'John'
        assert parsed_params['user']['photo'].__class__ is File