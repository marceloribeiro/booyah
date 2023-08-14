from lib.application.application_router import ApplicationRouter
import json

ROUTES_FILE = 'config/routes.json'

class ApplicationRoutes:
    def __init__(self):
        self.application_router = ApplicationRouter.get_instance()
        routese_file = open(ROUTES_FILE)
        routes = json.load(routese_file)

        for route in routes:
            self.application_router.add_route(route)
            print('DEBUG Registering route', route)

        routese_file.close()

    def load_routes():
        if not hasattr(ApplicationRoutes, "_instance"):
            ApplicationRoutes._instance = ApplicationRoutes()
        return ApplicationRoutes._instance