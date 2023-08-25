import importlib
import re
from booyah.helpers.application_helper import to_camel_case
from booyah.logger import logger

DEFAULT_CONTROLLER_NAME = 'application_controller'
DEFAULT_ACTION_NAME = 'index'
DEFAULT_RESPONSE_FORMAT = 'html'
CONTROLLER_SUFFIX = '_controller'
RESPONSE_FORMAT_HTML = 'html'
RESPONSE_FORMAT_TEXT = 'text'
RESPONSE_FORMAT_JSON = 'json'

def get_controller_action(route_data, environment):
    set_response_format(route_data, environment)

    if route_data.get('controller') != None:
        return get_controller_action_from_string(route_data['controller'], environment)
    if route_data['to'] != None:
        return get_controller_action_from_string(route_data['to'], environment)

    return None

def set_response_format(route_data, environment):
    format_from_header = get_format_from_content_type(environment.get('HTTP_ACCEPT'))

    if route_data.get('format') != None:
        environment['RESPONSE_FORMAT'] = route_data['format']
    elif format_from_header != None:
        environment['RESPONSE_FORMAT'] = format_from_header
    else:
        environment['RESPONSE_FORMAT'] = DEFAULT_RESPONSE_FORMAT

    environment['CONTENT_TYPE'] = content_type_from_response_format(environment['RESPONSE_FORMAT'])
    return environment['RESPONSE_FORMAT']

def content_types():
    return {
        RESPONSE_FORMAT_HTML: 'text/html',
        RESPONSE_FORMAT_JSON: 'application/json',
        RESPONSE_FORMAT_TEXT: 'text/plain'
    }

def content_type_from_response_format(response_format):
    return content_types().get(response_format, 'text/html')

def get_format_from_content_type(http_accept):
    content_type = http_accept.split(',')[0]
    formats = { content_type: format for format, content_type in content_types().items() }
    return formats.get(content_type, RESPONSE_FORMAT_HTML)

def get_controller_action_from_string(controller_string, environment):
    controller_name = DEFAULT_CONTROLLER_NAME
    action_name = DEFAULT_ACTION_NAME

    parts = controller_string.split('.')
    module_name = '.'.join(parts[:-1])
    if not module_name:
        module_name = 'booyah.controllers'
    controller_action = parts[-1]

    if re.search('#', controller_action):
        parts = controller_action.split('#')
        controller_name = parts[0] + CONTROLLER_SUFFIX
        action_name = parts[1]
    else:
        controller_name = controller_action + CONTROLLER_SUFFIX

    module = importlib.import_module(module_name + '.' + controller_name)
    controller_class = getattr(module, to_camel_case(controller_name))

    environment['controller_name'] = controller_name.replace(CONTROLLER_SUFFIX, '')
    environment['action_name'] = action_name

    logger.debug('Processing:', controller_class.__name__, '=>', action_name)
    return controller_class(environment).get_action(action_name)