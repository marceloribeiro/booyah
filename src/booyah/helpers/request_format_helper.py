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

    def respond_to(self, html_block=None, json_block=None, text_block=None):
        if html_block is not None and ContentType.HTML.value in self.http_accept:
            self.environment['CONTENT_TYPE'] = ContentType.HTML.value
            return html_block()
        if json_block is not None and ContentType.JSON.value in self.http_accept:
            self.environment['CONTENT_TYPE'] = ContentType.JSON.value
            return json_block()
        if text_block is not None and ContentType.TEXT.value in self.http_accept:
            self.environment['CONTENT_TYPE'] = ContentType.TEXT.value
            return text_block()

        # if not included in accept, will return prior argument
        if html_block is not None:
            self.environment['CONTENT_TYPE'] = ContentType.HTML.value
            return html_block()
        if json_block is not None:
            self.environment['CONTENT_TYPE'] = ContentType.JSON.value
            return json_block()
        if text_block is not None:
            self.environment['CONTENT_TYPE'] = ContentType.TEXT.value
            return text_block()