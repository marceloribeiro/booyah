from booyah.config.routes import routes
from booyah.router.routes_manager import METHOD_INDEX, URL_PATH_INDEX, ROUTE_NAME_INDEX, FULL_PATH_INDEX, FORMAT_INDEX

class TestApplicationRoutes:
    def test_it_loads_routes(self):
        assert(len(routes) == 12)
        assert(routes[0][URL_PATH_INDEX] == '/users')
        assert(routes[1][URL_PATH_INDEX] == '/users/<int:id>')
        assert(routes[1][FULL_PATH_INDEX] == 'booyah.controllers.users_controller#show')
        assert(routes[9][FORMAT_INDEX] == 'json')
        assert(routes[9][FULL_PATH_INDEX] == 'booyah.controllers.home_controller#status')
        assert(routes[9][URL_PATH_INDEX] == '/status')