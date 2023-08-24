from booyah.router.application_router import ApplicationRouter
import json
from booyah.logger import logger

ROUTES_FILE_PATH = 'config/routes.json'

class ApplicationRoutes:
    def __init__(self, routes_file_path=ROUTES_FILE_PATH):
        self.application_router = ApplicationRouter.get_instance()
        routes_file = open(routes_file_path)
        routes = json.load(routes_file)

        for route in routes:
            self.application_router.add_route(route)
            logger.debug('Registering route:', route)

        routes_file.close()

    def load_routes():
        if not hasattr(ApplicationRoutes, "_instance"):
            ApplicationRoutes._instance = ApplicationRoutes()
        return ApplicationRoutes._instance