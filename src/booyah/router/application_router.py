from booyah.router.application_route import ApplicationRoute
from booyah.response.application_response import ApplicationResponse
from booyah.response.asset_response import AssetResponse
from booyah.response.public_response import PublicResponse
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
            if route.exact_match(environment):
                return get_controller_action(route.route_data, environment)

        for route in self.routes:
            if route.match(environment):
                return get_controller_action(route.route_data, environment)
        return None

    def respond(self, environment):
        logger.debug(environment['REQUEST_METHOD'] + ':', environment['PATH_INFO'])

        if environment['PATH_INFO'].startswith("/assets"):
            return AssetResponse(environment)

        controller_action_dict = self.action(environment)

        if not controller_action_dict:
            return PublicResponse(environment)

        controller = controller_action_dict['controller']
        action = controller_action_dict['action']
        if controller and action:
            response = controller.run_action(action)
        else:
            response = self.not_found(environment)
        return response

    def not_found(self, environment):
        response = ApplicationResponse(environment,f"No routes matches [{environment['REQUEST_METHOD']}] \"{environment['PATH_INFO']}\"", status='404 Not Found')
        return response