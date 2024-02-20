import re

class RouteMatcher:
    def __init__(self, route_pattern):
        self.route_pattern = route_pattern

    def is_valid_url(self, check_url):
        url = self.remove_trailing_slash(check_url)
        escaped_pattern = re.escape(self.route_pattern)
        
        param_pattern = r'<(?P<datatype>\w+):(?P<param_name>\w+)>'
        escaped_pattern = re.sub(param_pattern, r'(?P<\2>[^/]+)', escaped_pattern)

        escaped_pattern = f"^{escaped_pattern}$"
        route_pattern = re.compile(escaped_pattern)
        match = route_pattern.match(url)

        return match is not None

    def remove_trailing_slash(self, url):
        if len(url) > 1 and url.endswith('/'):
            return url[:-1]
        else:
            return url

    def build_params(self, check_url):
        url = self.remove_trailing_slash(check_url)
        escaped_pattern = re.escape(self.route_pattern)
        
        param_pattern = r'<(?P<datatype>\w+):(?P<param_name>\w+)>'
        escaped_pattern = re.sub(param_pattern, r'(?P<\2>[^/]+)', escaped_pattern)

        escaped_pattern = f"^{escaped_pattern}$"
        route_pattern = re.compile(escaped_pattern)
        match = route_pattern.match(url)
        if match:
            params = {}
            for param in re.finditer(param_pattern, self.route_pattern):
                param_name = param.group('param_name')
                param_value = match.group(param_name)
                if param.group('datatype') == 'int' and param_value.isdigit():
                    params[param_name] = int(param_value)
                else:
                    params[param_name] = param_value
            return params
        else:
            return None