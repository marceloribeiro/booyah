from booyah.router.application_router import ApplicationRouter
from booyah.logger import logger
import importlib.util
import os

class ApplicationRoutes:
    def __init__(self):
        self.application_router = ApplicationRouter.get_instance()
        file_path = os.path.join(os.environ["ROOT_PROJECT_PATH"], 'config', 'routes.py')
        spec = importlib.util.spec_from_file_location("config.routes", file_path)
        file_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(file_module)
        
        for route in file_module.routes:
            self.application_router.add_route(route)
            logger.debug('Registering route:', route)

    def load_routes():
        if not hasattr(ApplicationRoutes, "_instance"):
            ApplicationRoutes._instance = ApplicationRoutes()
        return ApplicationRoutes._instance