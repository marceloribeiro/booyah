from booyah.config.routes import routes

class TestApplicationRoutes:
    def test_it_loads_routes(self):
        assert(len(routes) == 4)
        assert(routes[1]["format"] == 'json')
        assert(routes[1]["action"] == 'booyah.controllers.home_controller#status')
        assert(routes[1]["url"] == '/status')