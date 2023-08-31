from booyah.controllers.users_controller import UsersController
from booyah.models.user import User
from booyah.helpers.request_format_helper import ContentType
import io
import os

class TestUsersController:
    def setup_method(self):
        self._http_method = 'GET'
        self._query_string = ''
        self._wsgi_input = None
        self._matching_route = '/users'
        self._matching_route_params = []
        self._content_length = 0
        self._response_format = 'html'
        self._action_name = 'index'
        self._http_accept = ContentType.HTML.value

    def environment(self):
        return {
          'REQUEST_METHOD': self._http_method,
          'QUERY_STRING': self._query_string,
          'CONTENT_LENGTH': self._content_length,
          'CONTENT_TYPE': ContentType.JSON.value,
          'wsgi.input': self._wsgi_input,
          'MATCHING_ROUTE': self._matching_route,
          'MATCHING_ROUTE_PARAMS': self._matching_route_params,
          'controller_name': 'users',
          'action_name': self._action_name,
          'HTTP_ACCEPT': self._http_accept,
          'RESPONSE_FORMAT': self._response_format
        }

    # INDEX *******************************************************
    def test_should_return_html_users(self):
        User.create({"name": 'UserName', "email": "user@email.com"})
        controller = UsersController(self.environment())
        returned = controller.index()
        decoded_body = returned.response_body().decode('utf-8')
        assert "<table" in decoded_body
        assert "UserName" in decoded_body
        assert "user@email.com" in decoded_body

    def test_should_return_json_users(self):
        self._response_format = 'json'

        User.create({"name": 'UserName', "email": "user@email.com"})
        controller = UsersController(self.environment())
        returned = controller.index()
        decoded_body = returned.response_body().decode('utf-8')
        assert "<table" not in decoded_body
        assert "\"name\": \"UserName" in decoded_body
        assert "user@email.com" in decoded_body

    # SHOW *******************************************************
    def test_should_return_html_user(self):
        self._action_name = "show"

        user = User.create({"name": 'UserName', "email": "user@email.com"})
        controller = UsersController(self.environment())
        controller.params = { "id": user.id }
        returned = controller.show()
        decoded_body = returned.response_body().decode('utf-8')
        assert "<h1>Show User</h1>" in decoded_body
        assert f"/users/{user.id}/edit" in decoded_body
        assert "UserName" in decoded_body
        assert "user@email.com" in decoded_body

    def test_should_return_json_user(self):
        self._response_format = 'json'
        self._action_name = "show"

        user = User.create({"name": 'UserName', "email": "user@email.com"})
        controller = UsersController(self.environment())
        controller.params = { "id": user.id }
        returned = controller.show()
        decoded_body = returned.response_body().decode('utf-8')
        assert "<h1" not in decoded_body
        assert "\"name\": \"UserName" in decoded_body
        assert "user@email.com" in decoded_body

    # EDIT *******************************************************
    def test_should_return_html_edit_user(self):
        self._action_name = "edit"

        user = User.create({"name": 'UserName', "email": "user@email.com"})
        controller = UsersController(self.environment())
        controller.params = { "id": user.id }
        returned = controller.edit()
        decoded_body = returned.response_body().decode('utf-8')
        assert "<h1>Edit User</h1>" in decoded_body
        assert "UserName" in decoded_body
        assert "user@email.com" in decoded_body

    # NEW *******************************************************
    def test_should_return_html_new_user(self):
        self._action_name = "new"

        controller = UsersController(self.environment())
        returned = controller.new()
        decoded_body = returned.response_body().decode('utf-8')
        assert "<h1>New User</h1>" in decoded_body


    # CREATE *******************************************************
    def test_should_return_redirect_to_new_user(self):
        self._action_name = "create"

        count_before = User.count()
        controller = UsersController(self.environment())
        controller.params = {"user": {"name": 'UserName', "email": "user@email.com"}}
        returned = controller.create()
        decoded_body = returned.response_body().decode('utf-8')
        
        assert User.count() == count_before + 1
        assert decoded_body == ''
        assert returned.response_headers() == [('Location', f'/users/{User.last().id}')]

    def test_should_return_created_user_json(self):
        self._response_format = 'json'
        self._action_name = "create"
        self._http_accept = ContentType.JSON.value
        
        count_before = User.count()
        controller = UsersController(self.environment())
        controller.params = {"user": {"name": 'CreatedUser', "email": "user@email.com"}}
        returned = controller.create()
        decoded_body = returned.response_body().decode('utf-8')
        
        assert User.count() == count_before + 1
        assert "\"name\": \"CreatedUser" in decoded_body
        assert "user@email.com" in decoded_body


    # UPDATE *******************************************************
    def test_should_return_redirect_to_updated_user(self):
        self._action_name = "update"

        user = User.create({"name": 'UserName', "email": "user@email.com"})
        controller = UsersController(self.environment())
        controller.params = {"id": user.id, "user": {"name": 'NameChanged', "email": "user@email.com"}}
        returned = controller.update()
        decoded_body = returned.response_body().decode('utf-8')
        
        assert decoded_body == ''
        assert User.find(user.id).name == 'NameChanged'
        assert returned.response_headers() == [('Location', f'/users/{user.id}')]

    def test_should_return_updated_user_json(self):
        self._response_format = 'json'
        self._action_name = "update"
        self._http_accept = ContentType.JSON.value
        
        user = User.create({"name": 'UserName', "email": "user@email.com"})
        controller = UsersController(self.environment())
        controller.params = {"id": user.id, "user": {"name": 'NameChanged', "email": "user@email.com"}}
        returned = controller.update()
        decoded_body = returned.response_body().decode('utf-8')
        
        assert User.find(user.id).name == 'NameChanged'
        assert "\"name\": \"NameChanged" in decoded_body

    # DESTROY *******************************************************
    def test_should_return_redirect_to_index(self):
        self._action_name = "destroy"

        user = User.create({"name": 'UserName', "email": "user@email.com"})
        controller = UsersController(self.environment())
        controller.params = { "id": user.id }
        returned = controller.destroy()
        decoded_body = returned.response_body().decode('utf-8')
        assert decoded_body == ''
        assert len(User.where("id", user.id)) == 0

    def test_should_return_destroy_user_response(self):
        self._response_format = 'json'
        self._action_name = "destroy"
        self._http_accept = ContentType.JSON.value

        user = User.create({"name": 'UserName', "email": "user@email.com"})
        controller = UsersController(self.environment())
        controller.params = { "id": user.id }
        returned = controller.destroy()
        decoded_body = returned.response_body().decode('utf-8')
        assert len(User.where("id", user.id)) == 0
        assert decoded_body == '{"deleted": true, "deleted_id": ' + str(user.id) + '}'
