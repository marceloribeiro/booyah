from booyah.router.application_router import ApplicationRouter
from booyah.controllers.application_controller import ApplicationController

class UsersController(ApplicationController):
    def index(self):
        return self.render({'text': 'Users Controller, Index Action'})
    def show(self):
        return self.render({'text': 'Users Controller, Show Action'})

class TestApplicationRouter:
    def setup_method(self):
        self.router = ApplicationRouter()
        self.environment = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/users',
            'QUERY_STRING': 'test=1',
            'HTTP_ACCEPT': 'text/html;q=0.9,application/json;q=0.8,text/plain;q=0.7',
            'MATCHING_ROUTE': '/users',
            'MATCHING_ROUTE_PARAMS': [],
        }
        self.first_route = {
            'get': '/users', 'to': 'users#index', 'format': 'html'
        }
        self.second_route = {
            'get': '/users/1', 'to': 'users#show', 'format': 'html'
        }

    def test_init(self):
        assert self.router.routes == []

    def test_add_route(self):
        self.router.add_route(self.first_route)
        assert len(self.router.routes) == 1
        assert self.router.routes[0].route_data == self.first_route
        self.router.add_route(self.second_route)
        assert len(self.router.routes) == 2
        assert self.router.routes[0].route_data == self.first_route
        assert self.router.routes[1].route_data == self.second_route