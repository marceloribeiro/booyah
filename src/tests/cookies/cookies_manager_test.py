from booyah.cookies.cookies_manager import CookiesManager
from datetime import timedelta, datetime
import time

class TestCookiesManager:
    def test_empty_init(self):
        environment = {}
        cookies_manager = CookiesManager()
        cookies_manager.initialize(environment)
        assert cookies_manager.get_all_cookies() == {}

    def test_init_with_cookie(self):
        environment = {'HTTP_COOKIE': 'username=johndoe; sessionid=abc123'}
        cookies_manager = CookiesManager()
        cookies_manager.initialize(environment)
        all_cookies = cookies_manager.get_all_cookies()
        assert not all_cookies == {}
        assert all_cookies['username'] == 'johndoe'
        assert all_cookies['sessionid'] == 'abc123'
    
    def test_set_cookie_expiration(self):
        environment = {}
        cookies_manager = CookiesManager()
        cookies_manager.initialize(environment)
        expiration_time = datetime.utcnow() + timedelta(seconds=1)
        cookies_manager.set_cookie('abc', '123', expires=expiration_time)
        assert cookies_manager.get_all_cookies()['abc'] == '123'
        time.sleep(1.1)
        assert 'abc' not in cookies_manager.get_all_cookies()
    
    def test_get_cookie(self):
        environment = {}
        cookies_manager = CookiesManager()
        cookies_manager.initialize(environment)
        expiration_time = datetime.utcnow() + timedelta(seconds=1)
        cookies_manager.set_cookie('abc', '123', expires=expiration_time)
        assert cookies_manager.get_cookie('abc') == '123'

    def test_get_expired_cookie(self):
        environment = {}
        cookies_manager = CookiesManager()
        cookies_manager.initialize(environment)
        expiration_time = datetime.utcnow() - timedelta(seconds=1)
        cookies_manager.set_cookie('abc', '123', expires=expiration_time)
        assert cookies_manager.get_cookie('abc') == None

    def test_has_cookie(self):
        environment = {}
        cookies_manager = CookiesManager()
        cookies_manager.initialize(environment)
        cookies_manager.set_cookie('abc', '123')
        assert cookies_manager.has_cookie('abc') == True
        assert cookies_manager.has_cookie('abcdef') == False

    def test_create_session(self):
        environment = {}
        cookies_manager = CookiesManager()
        cookies_manager.initialize(environment)
        cookies_manager.create_session()
        assert cookies_manager.has_cookie('sessionid') == True
        assert len(cookies_manager.get_cookie('sessionid')) == 36

    def test_delete_cookie(self):
        environment = {}
        cookies_manager = CookiesManager()
        cookies_manager.initialize(environment)
        cookies_manager.set_cookie('abc', '123')
        assert cookies_manager.has_cookie('abc') == True
        assert cookies_manager.get_cookie('abc') == '123'
        cookies_manager.delete_cookie('abc')
        assert cookies_manager.has_cookie('abc') == False
        assert cookies_manager.get_cookie('abc') == None
        assert cookies_manager.is_expired(cookies_manager.cookies.get('abc')) == True

    def test_get_all_cookies(self):
        environment = {}
        cookies_manager = CookiesManager()
        cookies_manager.initialize(environment)
        expiration_time = datetime.utcnow() + timedelta(seconds=1)
        cookies_manager.set_cookie('abc', '123', expires=expiration_time)
        cookies_manager.set_cookie('def', '456')
        expired_time = datetime.utcnow() - timedelta(seconds=1)
        cookies_manager.set_cookie('ghi', '789', expires=expired_time)
        all_cookies = cookies_manager.get_all_cookies()
        assert len(all_cookies) == 2
        assert all_cookies['abc'] == '123'
        assert all_cookies['def'] == '456'
        

    def test_apply_cookies(self):
        environment = {}
        cookies_manager = CookiesManager()
        cookies_manager.initialize(environment)
        expiration_time = datetime.utcnow() + timedelta(seconds=1)
        cookies_manager.set_cookie('abc', '123', expires=expiration_time)
        cookies_manager.set_cookie('def', '456')
        expired_time = datetime.utcnow() - timedelta(seconds=1)
        cookies_manager.set_cookie('ghi', '789', expires=expired_time)
        response_headers = [('Content-Type', 'application/json')]
        cookies_manager.apply_cookies(response_headers)

        assert len(response_headers) == 2
        assert response_headers[0] == ('Content-Type', 'application/json')
        assert 'abc=123; expires=' in response_headers[1][1]
        assert 'def=456; expires=' in response_headers[1][1]
        assert '; HttpOnly; Path=/;' in response_headers[1][1]
        assert 'ghi=789; expires=' in response_headers[1][1]