import re
from booyah.router.routes_manager import FORMAT_INDEX, URL_PATH_INDEX, METHOD_INDEX, FULL_PATH_INDEX
from booyah.router.route_matcher import RouteMatcher

class ApplicationRoute:
    def __init__(self, route_data) -> None:
        self.route_data = route_data
        self.regex_pattern = None
        
        if self.route_data[FORMAT_INDEX] == '*':
            self.format = 'html'
        else:
            self.format = self.route_data[FORMAT_INDEX]

    def _compile_regex(self, pattern):
        pattern = re.sub(r'{\w+}', r'(.*)', pattern)
        return re.compile(f'^{pattern}$')

    def exact_match(self, environment):
        http_method = environment['REQUEST_METHOD'].upper()
        path_info = environment['PATH_INFO']

        if http_method != self.route_data[METHOD_INDEX]:
            return False
        
        if path_info == self.route_data[URL_PATH_INDEX]:
            environment['MATCHING_ROUTE_PARAMS'] = {}
            return True

        return False

    def match(self, environment):
        http_method = environment['REQUEST_METHOD'].upper()
        path_info = environment['PATH_INFO']

        if http_method != self.route_data[METHOD_INDEX]:
            return False

        route_pattern = self.route_data[URL_PATH_INDEX]
        matcher = RouteMatcher(route_pattern)

        if matcher.is_valid_url(path_info):
            environment['MATCHING_ROUTE_PARAMS'] = matcher.build_params(path_info)
            return True

        return False