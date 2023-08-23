from booyah.response.application_response import ApplicationResponse
import json
from booyah.logger import logger

class ApplicationController:
    def __init__(self, environment):
        self.environment = environment
        self.params = {}

    def get_action(self, action):
        return getattr(self, action)

    def load_params(self):
        self.load_params_from_route()
        self.load_params_from_query_string()
        self.load_params_from_gunicorn_body()
        logger.debug("PARAMS:", self.params)

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
        if query_string:
            for param in query_string.split('&'):
                key, value = param.split('=')
                params[key] = value
        self.params.update(params)

    def load_params_from_gunicorn_body(self):
        if self.environment.get('CONTENT_LENGTH') is None:
            return

        content_length = int(self.environment['CONTENT_LENGTH'])
        content_type = self.environment['CONTENT_TYPE']

        body_params = {}
        if content_length:
            body = self.environment['wsgi.input'].read(content_length)
            if content_type == 'application/json':
                try:
                    body_json = body.decode('utf-8')
                except:
                    body_json = body
                body_params = json.loads(body_json)
            else:
                for param in body.decode('utf-8').split('&'):
                    key, value = param.split('=')
                    body_params[key] = value
        self.params.update(body_params)

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