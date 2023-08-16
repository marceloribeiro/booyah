import re

class ApplicationRoute:
    def __init__(self, route_data) -> None:
        self.route_data = route_data
        self.regex_pattern = None
        if 'format' in self.route_data.keys():
            self.format = self.route_data['format']
        else:
            self.format = 'html'

    def _compile_regex(self, pattern):
        pattern = re.sub(r'{\w+}', r'(.*)', pattern)
        return re.compile(f'^{pattern}$')

    def match(self, environment):
        http_method = environment['REQUEST_METHOD'].lower()
        path_info = environment['PATH_INFO']

        if http_method not in self.route_data.keys():
            return False
        if self.route_data.get(http_method) is None:
            return False

        if path_info != '/':
            path_info = re.sub(r'/$', '', re.sub(r'/\?', '?', path_info))

        self.regex_pattern = self._compile_regex(self.route_data[http_method])
        match = self.regex_pattern.match(path_info)

        if match:
            environment['MATCHING_ROUTE'] = self.route_data[http_method]
            environment['MATCHING_ROUTE_PARAMS'] = match.groups()
            return True

        return False