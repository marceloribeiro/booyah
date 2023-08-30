class RequestFormatHelper:
    def __init__(self, environment):
        if 'HTTP_ACCEPT' in environment:
            self.http_accept = environment['HTTP_ACCEPT']
        else:
            raise ValueError("Missing http accept header")
    
    def respond_to(self, html=None, json=None, text=None):
        if html is not None and 'text/html' in self.http_accept:
            return html()
        if json is not None and 'application/json' in self.http_accept:
            return json()
        if text is not None and 'text/plain' in self.http_accept:
            return text()
        
        # if not included in accept, will return prior argument
        if html is not None:
            return html()
        if json is not None:
            return json()
        if text is not None:
            return text()