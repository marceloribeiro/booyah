from booyah.response.application_response import ApplicationResponse
from booyah.response.redirect_response import RedirectResponse
import json
from urllib.parse import parse_qs
from booyah.logger import logger
from booyah.helpers.request_format_helper import RequestFormatHelper, ContentType

class BooyahApplicationController:
    before_action_blocks = []
    after_action_blocks  = []
    around_action_blocks = []

    @classmethod
    def add_before_action(self, block):
        self.before_action_blocks.append(block)

    @classmethod
    def add_after_action(self, block):
        self.after_action_blocks.append(block)

    @classmethod
    def add_around_action(self, block):
        self.around_action_blocks.append(block)

    def before_action(self):
        for block in self.__class__.before_action_blocks:
            if type(block) == str:
                block = getattr(self, block)
            block()

    def after_action(self):
        for block in self.__class__.after_action_blocks:
            if type(block) == str:
                block = getattr(self, block)
            block()

    def around_action(self, action):
        for block in self.__class__.around_action_blocks:
            if type(block) == str:
                block = getattr(self, block)
            block(action)

    def __init__(self, environment, should_load_params=True):
        self.environment = environment
        self.params = {}
        self.application_response = None
        if should_load_params:
            self.load_params()

    def respond_to(self, html=None, json=None, text=None):
        return RequestFormatHelper(self.environment).respond_to(html, json, text)

    def run_action(self, action):
        self.before_action()
        if self.around_action_blocks:
            self.around_action(action)
        else:
            action()
        self.after_action()
        return self.application_response

    def get_action(self, action):
        return getattr(self, action)

    def load_params(self):
        self.load_params_from_route()
        self.load_params_from_query_string()
        self.load_params_from_gunicorn_body()
        logger.debug("PARAMS:", self.params)

    def load_params_from_route(self):
        self.params.update(self.environment['MATCHING_ROUTE_PARAMS'])

    def load_params_from_query_string(self):
        query_string = self.environment['QUERY_STRING']
        params = {}
        if query_string:
            for param in query_string.split('&'):
                key, value = param.split('=')
                params[key] = value
        self.params.update(params)

    def parse_nested_attributes(self, body_data):
        parsed_data = parse_qs(body_data)
        nested_data = {}
        for key, value in parsed_data.items():
            keys = key.split("[")
            current_dict = nested_data
            for k in keys[:-1]:
                current_dict = current_dict.setdefault(k, {})

            if len(keys) == 1:
                current_dict[keys[-1]] = value[0]
            else:
                current_dict[keys[-1][:-1]] = value[0]

        return nested_data

    def load_params_from_gunicorn_body(self):
        if self.environment.get('CONTENT_LENGTH') is None or 'CONTENT_TYPE' not in self.environment:
            return

        content_type = self.environment['CONTENT_TYPE']
        content_length = int(self.environment['CONTENT_LENGTH'])

        body_params = {}
        if content_length:
            body = self.environment['wsgi.input'].read(content_length)
            if content_type == ContentType.JSON.value:
                try:
                    body_json = body.decode('utf-8')
                except:
                    body_json = body
                body_params = json.loads(body_json)
            elif content_type == ContentType.FORM_URLENCODED.value:
                body_params = self.parse_nested_attributes(str(body.decode('utf-8')))
            elif ContentType.MULTIPART.value in content_type:
                raise ValueError(f"{ContentType.MULTIPART.value} not supported yet, see ApplicationController load_params_from_gunicorn_body")
            else:
                for param in body.decode('utf-8').split('&'):
                    key, value = param.split('=')
                    body_params[key] = value
        self.params.update(body_params)

    def render(self, data = {}):
        self.application_response = ApplicationResponse(self.environment, data)
        return self.application_response

    def redirect(self, redirect_to):
        return RedirectResponse(self.environment, redirect_to)

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