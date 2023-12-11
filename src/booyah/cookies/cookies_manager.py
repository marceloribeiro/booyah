from http.cookies import SimpleCookie
from datetime import datetime, timedelta
import uuid

DEFAULT_EXPIRATION = timedelta(days=365)

class CookiesManager:
    def __init__(self, environment):
        self.cookies = SimpleCookie()
        self.environment = environment or {}

        if 'Cookie' in self.environment:
            self.cookies.load(self.environment['Cookie'])
        if 'HTTP_COOKIE' in self.environment:
            self.cookies.load(self.environment['HTTP_COOKIE'])

    @classmethod
    def add_to(self, environment):
        environment['cookies_manager'] = CookiesManager(environment)
        return environment['cookies_manager']
    
    @classmethod
    def from_environment(self, environment):
        return environment['cookies_manager']
    
    def set_cookie(self, key, value, max_age=None, expires=None, path='/', domain=None, secure=False, http_only=True, same_site=None):
        self.cookies[key] = value

        if max_age is not None:
            self.cookies[key]['max-age'] = max_age
        elif expires is not None:
            if isinstance(expires, datetime):
                self.cookies[key]['expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
            else:
                self.cookies[key]['expires'] = expires
        else:
            self.cookies[key]['expires'] = (datetime.utcnow() + DEFAULT_EXPIRATION).strftime('%a, %d %b %Y %H:%M:%S GMT')

        self.cookies[key]['path'] = path

        if domain is not None:
            self.cookies[key]['domain'] = domain

        if secure:
            self.cookies[key]['secure'] = True

        if http_only:
            self.cookies[key]['httponly'] = True

        if same_site is not None:
            self.cookies[key]['samesite'] = same_site

    def get_cookie(self, key):
        cookie = self.cookies.get(key, None)
        if not cookie == None and not self.is_expired(cookie):
            return cookie.value
        return None

    def create_session(self):
        sessionid = str(uuid.uuid4())
        self.set_cookie('sessionid', sessionid, secure=True, http_only=True)
        return sessionid
    
    def has_cookie(self, key):
        return key in self.get_all_cookies()

    def delete_cookie(self, key, path='/', domain=None):
        self.set_cookie(key, '', expires='Thu, 01 Jan 1970 00:00:00 GMT', path=path, domain=domain)
    
    def is_expired(self, cookie):
        cookie_instance = cookie
        if isinstance(cookie, str):
            cookie_instance = self.cookies[cookie]
        if not cookie_instance.get('expires'):
            return False
        current_time = datetime.utcnow()
        if isinstance(cookie_instance.get('expires'), datetime) and current_time <= cookie_instance['expires']:
            return False
        elif isinstance(cookie_instance.get('expires'), str) and current_time <= datetime.strptime(cookie_instance['expires'], '%a, %d %b %Y %H:%M:%S GMT'):
            return False
        return True

    def get_all_cookies(self):
        all_cookies = {}

        for key, cookie in self.cookies.items():
            if not self.is_expired(cookie):
                all_cookies[key] = cookie.value

        return all_cookies

    def apply_cookies(self, target_array):
        target_array.append(('Set-Cookie', self.cookies.output(header='', sep='; ')))
        return target_array