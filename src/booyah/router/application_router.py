from booyah.router.application_route import ApplicationRoute
from booyah.response.application_response import ApplicationResponse
from booyah.helpers.controller_helper import get_controller_action
from booyah.logger import logger

class ApplicationRouter:
    def __init__(self):
        self.routes = []

    def get_instance():
        if not hasattr(ApplicationRouter, "_instance"):
            ApplicationRouter._instance = ApplicationRouter()
        return ApplicationRouter._instance

    def add_route(self, route_data):
        route = ApplicationRoute(route_data)
        self.routes.append(route)

    def action(self, environment):
        for route in self.routes:
            if route.match(environment):
                return get_controller_action(route.route_data, environment)
        return None

    def respond(self, environment):
        logger.debug(environment['REQUEST_METHOD'] + ':', environment['PATH_INFO'])
        controller_action = self.action(environment)

        if controller_action:
            response = controller_action()
        else:
            response = self.not_found(environment)

        return response

    def not_found(self, environment):
        response = ApplicationResponse(environment, 'Not Found')
        return response