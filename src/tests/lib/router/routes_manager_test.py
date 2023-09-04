from booyah.router.routes_manager import *

class TestRoutesManager:
    def setup_method(self):
        self.manager = RoutesManager()

    def test_init(self):
        assert len(self.manager.routes) == 0

    def test_add_get_route(self):
        self.manager.get('/test', 'test_path', 'test#index')
        assert self.manager.routes[-1] == ('GET', '/test', 'test_path', 'test_controller#index', '*')

    def test_add_post_route(self):
        self.manager.post('/test', 'test_path', 'test#index')
        assert self.manager.routes[-1] == ('POST', '/test', 'test_path', 'test_controller#index', '*')

    def test_add_put_route(self):
        self.manager.put('/test', 'test_path', 'test#index')
        assert self.manager.routes[-1] == ('PUT', '/test', 'test_path', 'test_controller#index', '*')

    def test_add_patch_route(self):
        self.manager.patch('/test', 'test_path', 'test#index')
        assert self.manager.routes[-1] == ('PATCH', '/test', 'test_path', 'test_controller#index', '*')

    def test_add_delete_route(self):
        self.manager.delete('/test', 'test_path', 'test#index')
        assert self.manager.routes[-1] == ('DELETE', '/test', 'test_path', 'test_controller#index', '*')

    def test_add_resources_route(self):
        self.manager.routes = []
        self.manager.resources('users', 'booyah.controllers')

        assert self.manager.routes == [
            ('GET',     '/users',               'user_index',   'booyah.controllers.users_controller#index', '*'),
            ('GET',     '/users/<int:id>',      'user_show',    'booyah.controllers.users_controller#show', '*'),
            ('GET',     '/users/new',           'user_new',     'booyah.controllers.users_controller#new', '*'),
            ('POST',    '/users',               'user_create',  'booyah.controllers.users_controller#create', '*'),
            ('GET',     '/users/<int:id>/edit', 'user_edit',    'booyah.controllers.users_controller#edit', '*'),
            ('PUT',     '/users/<int:id>',      'user_update',  'booyah.controllers.users_controller#update', '*'),
            ('PATCH',   '/users/<int:id>',      'user_update',  'booyah.controllers.users_controller#update', '*'),
            ('DELETE',  '/users/<int:id>',      'user_destroy', 'booyah.controllers.users_controller#destroy', '*')
        ]

    def test_add_resources_with_parent_route(self):
        self.manager.routes = []
        self.manager.resources('messages', '', parent='/users/<int:id>')
        assert self.manager.routes == [
            ('GET',     '/users/<int:id>/messages',                 'message_index',    'messages_controller#index', '*'),
            ('GET',     '/users/<int:id>/messages/<int:id>',        'message_show',     'messages_controller#show', '*'),
            ('GET',     '/users/<int:id>/messages/new',             'message_new',      'messages_controller#new', '*'),
            ('POST',    '/users/<int:id>/messages',                 'message_create',   'messages_controller#create', '*'),
            ('GET',     '/users/<int:id>/messages/<int:id>/edit',   'message_edit',     'messages_controller#edit', '*'),
            ('PUT',     '/users/<int:id>/messages/<int:id>',        'message_update',   'messages_controller#update', '*'),
            ('PATCH',   '/users/<int:id>/messages/<int:id>',        'message_update',   'messages_controller#update', '*'),
            ('DELETE',  '/users/<int:id>/messages/<int:id>',        'message_destroy',  'messages_controller#destroy', '*')
        ]

