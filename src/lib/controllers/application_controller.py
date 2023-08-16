from lib.application.application_response import ApplicationResponse

class ApplicationController:
    def __init__(self, environment):
        self.environment = environment
        self.params = {}

    def get_action(self, action):
        self.load_params()
        return getattr(self, action)

    def load_params(self):
        self.load_params_from_route()
        self.load_params_from_query_string()
        print("PARAMS:", self.params)

    def load_params_from_route(self):
        matching_route = self.environment['MATCHING_ROUTE']
        matching_route_params = self.environment['MATCHING_ROUTE_PARAMS']
        params = {}

        if matching_route != None:
            parts = matching_route.split('/')
            position = 0
            for i, part in enumerate(parts):
                if part.startswith('{') and part.endswith('}'):
                    params[part[1:-1]] = matching_route_params[position]
                    position += 1
        self.params.update(params)

    def load_params_from_query_string(self):
        query_string = self.environment['QUERY_STRING']
        params = {}
        if query_string != '':
            for param in query_string.split('&'):
                key, value = param.split('=')
                params[key] = value
        self.params.update(params)

    def render(self, data = {}):
      return ApplicationResponse(self.environment, data)

    def is_get_request(self):
        return self.environment['REQUEST_METHOD'] == 'GET'

    def is_post_request(self):
        return self.environment['REQUEST_METHOD'] == 'POST'

    def is_put_request(self):
        return self.environment['REQUEST_METHOD'] == 'PUT'

    def is_delete_request(self):
        return self.environment['REQUEST_METHOD'] == 'DELETE'

    def is_patch_request(self):
        return self.environment['REQUEST_METHOD'] == 'PATCH'