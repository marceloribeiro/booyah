from booyah.router.route_matcher import RouteMatcher

class TestRouteMatcher:
    def test_valid_home_route(self):
        assert RouteMatcher('/').is_valid_url('/') == True

    def test_valid_route_param(self):
        assert RouteMatcher('/users/<int:id>').is_valid_url('/users/1') == True

    def test_ignore_param_datatype(self):
        assert RouteMatcher('/users/<int:id>').is_valid_url('/users/abc') == True

    def test_is_invalid_other_route_id(self):
        assert RouteMatcher('/messages/<int:id>').is_valid_url('/users/1') == False

    def test_exact_match_valid(self):
        assert RouteMatcher('/users/new').is_valid_url('/users/new') == True

    def test_exact_match_not_valid(self):
        assert RouteMatcher('/users/new').is_valid_url('/users/1') == False
    
    def test_extract_blank_params(self):
        assert RouteMatcher('/users/new').build_params('/users/new') == { }
    
    def test_extract_param_int(self):
        assert RouteMatcher('/users/<int:id>').build_params('/users/1') == { "id": 1 }
    
    def test_extract_invalid_param_int(self):
        assert RouteMatcher('/users/<int:id>').build_params('/users/new') == {}
    
    def test_extract_param_str(self):
        assert RouteMatcher('/users/<str:id>').build_params('/users/1') == { "id": "1" }
        assert RouteMatcher('/users/<str:action>').build_params('/users/new') == { "action": "new" }