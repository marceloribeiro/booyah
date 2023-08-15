import re

class ApplicationRoute:
    def __init__(self, route_data) -> None:
        self.route_data = route_data
        if 'format' in self.route_data.keys():
            self.format = self.route_data['format']
        else:
            self.format = 'html'

    def match(self, environment):
        http_method = environment['REQUEST_METHOD'].lower()
        if http_method not in self.route_data.keys():
            return False
        if self.route_data[http_method] == None:
            return False

        pattern = re.compile(self.route_data[http_method])
        if pattern.match(environment['RAW_URI']):
            return True
