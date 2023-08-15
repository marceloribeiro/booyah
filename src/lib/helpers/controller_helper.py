import importlib
import re
from lib.helpers.application_helper import to_camel_case

DEFAULT_CONTROLLER_NAME = 'application_controller'
DEFAULT_ACTION_NAME = 'index'
CONTROLLER_SUFFIX = '_controller'

def get_controller_action(route_data, environment):
    if route_data.get('controller') != None:
        return get_controller_action_from_string(route_data['controller'], environment)
    if route_data['to'] != None:
        return get_controller_action_from_string(route_data['to'], environment)

    return None

def get_controller_action_from_string(controller_string, environment):
    controller_name = DEFAULT_CONTROLLER_NAME
    action_name = DEFAULT_ACTION_NAME

    parts = controller_string.split('.')
    module_name = '.'.join(parts[:-1])
    if module_name == '':
        module_name = 'lib.application.controllers'
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

    print('DEBUG Processing: ' + controller_class.__name__ + ' => ' + action_name)
    return controller_class(environment).get_action(action_name)