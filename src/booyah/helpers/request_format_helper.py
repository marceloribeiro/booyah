from enum import Enum

class ContentType(Enum):
    JSON = "application/json"
    XML = "application/xml"
    FORM_URLENCODED = "application/x-www-form-urlencoded"
    TEXT = "text/plain"
    HTML = "text/html"
    MULTIPART = "multipart/form-data"

class RequestFormatHelper:
    def __init__(self, environment):
        self.environment = environment
        if 'HTTP_ACCEPT' in environment:
            self.http_accept = environment['HTTP_ACCEPT']
        else:
            raise ValueError("Missing http accept header")

    def respond_to(self, html=None, json=None, text=None):
        if html is not None and ContentType.HTML.value in self.http_accept:
            self.environment['CONTENT_TYPE'] = ContentType.HTML.value
            return html()
        if json is not None and ContentType.JSON.value in self.http_accept:
            self.environment['CONTENT_TYPE'] = ContentType.JSON.value
            return json()
        if text is not None and ContentType.TEXT.value in self.http_accept:
            self.environment['CONTENT_TYPE'] = ContentType.TEXT.value
            return text()

        # if not included in accept, will return prior argument
        if html is not None:
            self.environment['CONTENT_TYPE'] = ContentType.HTML.value
            return html()
        if json is not None:
            self.environment['CONTENT_TYPE'] = ContentType.JSON.value
            return json()
        if text is not None:
            self.environment['CONTENT_TYPE'] = ContentType.TEXT.value
            return text()