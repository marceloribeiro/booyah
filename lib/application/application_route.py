import importlib
import re

class ApplicationRoute:
    def __init__(self, route_data) -> None:
        self.route_data = route_data

    def match(self, environment):
        http_method = environment['REQUEST_METHOD'].lower()
        if http_method not in self.route_data.keys():
            return False
        if self.route_data[http_method] == None:
            return False

        pattern = re.compile(self.route_data[http_method])
        if pattern.match(environment['RAW_URI']):
            return True

    def get_controller_action(self, environment):
        if self.route_data.get('controller') != None:
            return self.get_controller_action_from_string(self.route_data['controller'], environment)
        if self.route_data['to'] != None:
            return self.get_controller_action_from_string(self.route_data['to'], environment)

        return None

    def to_camel_case(self, input_string):
        words = input_string.split('_')
        capitalized = []

        for word in words:
            capitalized.append(word.capitalize())

        return ''.join(capitalized)


    def get_controller_action_from_string(self, controller_string, environment):
        controller_name = 'application_controller'
        action_name = 'index'

        parts = controller_string.split('.')
        module_name = '.'.join(parts[:-1])
        if module_name == '':
            module_name = 'lib.application.controllers'
        controller_action = parts[-1]

        if re.search('#', controller_action):
            parts = controller_action.split('#')
            controller_name = parts[0] + '_controller'
            action_name = parts[1]
        else:
            controller_name = controller_action + '_controller'

        module = importlib.import_module(module_name + '.' + controller_name)
        controller_class = getattr(module, self.to_camel_case(controller_name))

        print('DEBUG Processing: ' + controller_class.__name__ + ' => ' + action_name)
        return controller_class(environment).get_action(action_name)