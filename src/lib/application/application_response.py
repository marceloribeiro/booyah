class ApplicationResponse:
    def __init__(self, environment, body, headers = {}, status = '200 OK'):
        self.environment = environment
        self.body = body
        self.headers = headers
        self.status = status

    def response_headers(self):
        if (self.headers != {}):
            return self.headers
        else:
          return [
              ('Content-type', 'text/plain'),
              ('Content-Length', str(len(self.body)))
          ]

    def response_body(self):
        return bytes(self.body, 'utf-8')