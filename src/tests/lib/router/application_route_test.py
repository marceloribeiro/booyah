from booyah.router.application_route import ApplicationRoute

class TestApplicationRoute:
    def setup_method(self):
        self.route_data = {
            'get': '/test', 'to': 'home#index', 'format': 'html'
        }
        self.environment = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/test',
            'QUERY_STRING': 'test=1',
        }
        self.route = ApplicationRoute(self.route_data)

    def test_init(self):
        assert self.route.route_data == self.route_data
        assert self.route.regex_pattern == None
        assert self.route.format == 'html'

    def test_true_match(self):
        assert self.route.match(self.environment) == True
        assert self.environment['MATCHING_ROUTE'] == '/test'
        assert self.environment['MATCHING_ROUTE_PARAMS'] == ()
        self.environment['PATH_INFO'] = '/test/'
        assert self.route.match(self.environment) == True
        assert self.environment['MATCHING_ROUTE'] == '/test'
        assert self.environment['MATCHING_ROUTE_PARAMS'] == ()
        self.environment['PATH_INFO'] = '/test/1'
        assert self.route.match(self.environment) == False

    def test_false_match(self):
        self.environment['REQUEST_METHOD'] = 'POST'
        assert self.route.match(self.environment) == False

    def test_false_match_with_no_route_data(self):
        self.route.route_data = {}
        assert self.route.match(self.environment) == False

    def test_false_match_with_no_route_data_for_http_method(self):
        self.route.route_data = { 'post': '/test', 'to': 'home#index' }
        assert self.route.match(self.environment) == False