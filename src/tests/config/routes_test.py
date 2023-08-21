from config.routes import ApplicationRoutes

class TestApplicationRoutes:
    def test_it_loads_routes_from_json_file(self):
        routes = ApplicationRoutes('tests/assets/routes.json')
        assert(routes.application_router.__class__.__name__ == 'ApplicationRouter')
        assert(len(routes.application_router.routes) == 8)
        assert(routes.application_router.routes[0].route_data['delete'] == '/users/{id}')
        assert(routes.application_router.routes[0].route_data['to'] == 'users#destroy')
        assert(routes.application_router.routes[0].route_data['format'] == 'json')
        assert(routes.application_router.routes[7].route_data['get'] == '/')
        assert(routes.application_router.routes[7].route_data['to'] == 'home#index')