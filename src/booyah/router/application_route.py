import re
from booyah.router.route_matcher import RouteMatcher

class ApplicationRoute:
    def __init__(self, route_data) -> None:
        self.route_data = route_data
        self.regex_pattern = None
        
        if self.route_data["format"] == '*':
            self.format = 'html'
        else:
            self.format = self.route_data["format"]

    def _compile_regex(self, pattern):
        pattern = re.sub(r'{\w+}', r'(.*)', pattern)
        return re.compile(f'^{pattern}$')

    def exact_match(self, environment):
        http_method = environment['REQUEST_METHOD'].upper()
        path_info = environment['PATH_INFO']

        if http_method != self.route_data["method"]:
            return False
        
        if path_info == self.route_data["url"]:
            environment['MATCHING_ROUTE_PARAMS'] = {}
            return True

        return False

    def match(self, environment):
        if len(self.route_data) < 5:
            return False
        http_method = environment['REQUEST_METHOD'].upper()
        path_info = environment['PATH_INFO']

        if http_method != self.route_data["method"]:
            return False

        route_pattern = self.route_data["url"]
        matcher = RouteMatcher(route_pattern)
        if matcher.is_valid_url(path_info):
            environment['MATCHING_ROUTE_PARAMS'] = matcher.build_params(path_info)
            return True

        return False