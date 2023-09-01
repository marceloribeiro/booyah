import re

class RouteMatcher:
    def __init__(self, route_pattern):
        self.route_pattern = route_pattern

    def is_valid_url(self, url):
        # Escape special characters in the route pattern
        escaped_pattern = re.escape(self.route_pattern)
        
        # Replace <datatype:param_name> with appropriate regex patterns
        param_pattern = r'<(?P<datatype>\w+):(?P<param_name>\w+)>'
        escaped_pattern = re.sub(param_pattern, r'(?P<\2>[^/]+)', escaped_pattern)

        # Add anchors to match the entire URL
        escaped_pattern = f"^{escaped_pattern}$"

        # Compile the modified route pattern
        route_pattern = re.compile(escaped_pattern)

        # Match the URL against the compiled pattern
        match = route_pattern.match(url)

        return match is not None

    def build_params(self, url):
        # Escape special characters in the route pattern
        escaped_pattern = re.escape(self.route_pattern)
        
        # Replace <datatype:param_name> with appropriate regex patterns
        param_pattern = r'<(?P<datatype>\w+):(?P<param_name>\w+)>'
        escaped_pattern = re.sub(param_pattern, r'(?P<\2>[^/]+)', escaped_pattern)

        # Add anchors to match the entire URL
        escaped_pattern = f"^{escaped_pattern}$"

        # Compile the modified route pattern
        route_pattern = re.compile(escaped_pattern)

        # Match the URL against the compiled pattern
        match = route_pattern.match(url)

        if match:
            # Extract parameters with their values and data types
            params = {}
            for param in re.finditer(param_pattern, self.route_pattern):
                param_name = param.group('param_name')
                param_value = match.group(param_name)
                if param.group('datatype') == 'int':
                    params[param_name] = int(param_value)
                else:
                    params[param_name] = param_value

            return params
        else:
            return None