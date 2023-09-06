from booyah.router.routes_manager import *

class TestRoutesManager:
    def setup_method(self):
        self.manager = RoutesManager()

    def test_init(self):
        assert len(self.manager.routes) == 0

    def test_add_get_route(self):
        self.manager.get('/test', 'test_path', 'test#index')
        assert self.manager.routes[-1] == {"method": 'GET', "url": '/test', "name": 'test_path', "action": 'test_controller#index', "format": '*'}

    def test_add_post_route(self):
        self.manager.post('/test', 'test_path', 'test#index')
        assert self.manager.routes[-1] == {"method": 'POST', "url": '/test', "name": 'test_path', "action": 'test_controller#index', "format": '*'}

    def test_add_put_route(self):
        self.manager.put('/test', 'test_path', 'test#index')
        assert self.manager.routes[-1] == {"method": 'PUT', "url": '/test', "name": 'test_path', "action": 'test_controller#index', "format": '*'}

    def test_add_patch_route(self):
        self.manager.patch('/test', 'test_path', 'test#index')
        assert self.manager.routes[-1] == {"method": 'PATCH', "url": '/test', "name": 'test_path', "action": 'test_controller#index', "format": '*'}

    def test_add_delete_route(self):
        self.manager.delete('/test', 'test_path', 'test#index')
        assert self.manager.routes[-1] == {"method": 'DELETE', "url": '/test', "name": 'test_path', "action": 'test_controller#index', "format": '*'}

    def test_add_resources_route(self):
        self.manager.routes = []
        self.manager.resources('users', 'booyah.controllers')

        assert self.manager.routes == [
            {"method": 'GET',     "url": '/users',               "name": 'user_index',   "action": 'booyah.controllers.users_controller#index', "format": '*'},
            {"method": 'GET',     "url": '/users/<int:id>',      "name": 'user_show',    "action": 'booyah.controllers.users_controller#show', "format": '*'},
            {"method": 'GET',     "url": '/users/new',           "name": 'user_new',     "action": 'booyah.controllers.users_controller#new', "format": '*'},
            {"method": 'POST',    "url": '/users',               "name": 'user_create',  "action": 'booyah.controllers.users_controller#create', "format": '*'},
            {"method": 'GET',     "url": '/users/<int:id>/edit', "name": 'user_edit',    "action": 'booyah.controllers.users_controller#edit', "format": '*'},
            {"method": 'PUT',     "url": '/users/<int:id>',      "name": 'user_update',  "action": 'booyah.controllers.users_controller#update', "format": '*'},
            {"method": 'PATCH',   "url": '/users/<int:id>',      "name": 'user_update',  "action": 'booyah.controllers.users_controller#update', "format": '*'},
            {"method": 'DELETE',  "url": '/users/<int:id>',      "name": 'user_destroy', "action": 'booyah.controllers.users_controller#destroy', "format": '*'}
        ]

    def test_add_resources_with_parent_route(self):
        self.manager.routes = []
        self.manager.resources('messages', '', parent='/users/<int:id>')
        assert self.manager.routes == [
            {"method": 'GET',     "url": '/users/<int:id>/messages',                 "name": 'message_index',    "action": 'messages_controller#index', "format": '*'},
            {"method": 'GET',     "url": '/users/<int:id>/messages/<int:id>',        "name": 'message_show',     "action": 'messages_controller#show', "format": '*'},
            {"method": 'GET',     "url": '/users/<int:id>/messages/new',             "name": 'message_new',      "action": 'messages_controller#new', "format": '*'},
            {"method": 'POST',    "url": '/users/<int:id>/messages',                 "name": 'message_create',   "action": 'messages_controller#create', "format": '*'},
            {"method": 'GET',     "url": '/users/<int:id>/messages/<int:id>/edit',   "name": 'message_edit',     "action": 'messages_controller#edit', "format": '*'},
            {"method": 'PUT',     "url": '/users/<int:id>/messages/<int:id>',        "name": 'message_update',   "action": 'messages_controller#update', "format": '*'},
            {"method": 'PATCH',   "url": '/users/<int:id>/messages/<int:id>',        "name": 'message_update',   "action": 'messages_controller#update', "format": '*'},
            {"method": 'DELETE',  "url": '/users/<int:id>/messages/<int:id>',        "name": 'message_destroy',  "action": 'messages_controller#destroy', "format": '*'}
        ]

