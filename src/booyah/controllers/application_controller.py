import json
from booyah.response.application_response import ApplicationResponse
from booyah.response.redirect_response import RedirectResponse
from urllib.parse import parse_qs
from booyah.logger import logger
from booyah.application_support.action_support import ActionSupport
from booyah.helpers.request_format_helper import RequestFormatHelper, ContentType, parse_header, parse_multipart
from booyah.cookies.cookies_manager import CookiesManager

class BooyahApplicationController(ActionSupport):
    def __init__(self, environment, should_load_params=True):
        self.cookies_manager = CookiesManager.add_to(environment)
        self.environment = environment
        if not self.cookies_manager.has_cookie('sessionid'):
            self.cookies_manager.create_session()
        self.params = {}
        self.application_response = None
        if should_load_params:
            self.load_params()

    def respond_to(self, html=None, json=None, text=None):
        return RequestFormatHelper(self.environment).respond_to(html, json, text)

    def load_params(self):
        self.load_params_from_route()
        self.load_params_from_query_string()
        self.load_params_from_gunicorn_body()
        logger.debug("PARAMS:", self.params)

    def load_params_from_route(self):
        if 'MATCHING_ROUTE_PARAMS' in self.environment:
            self.params.update(self.environment['MATCHING_ROUTE_PARAMS'])

    def load_params_from_query_string(self):
        query_string = None
        if 'QUERY_STRING' in self.environment:
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
                body_params = parse_multipart(self.environment, body)
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