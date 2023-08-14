from lib.application.application_response import ApplicationResponse

class ApplicationController:
    def __init__(self, environment):
        self.environment = environment

    def get_action(self, action):
        return getattr(self, action)

    def render(self, data):
      return ApplicationResponse(self.environment, data)

    def is_get_request(self):
        return self.environment['REQUEST_METHOD'] == 'GET'

    def is_post_request(self):
        return self.environment['REQUEST_METHOD'] == 'POST'

    def is_put_request(self):
        return self.environment['REQUEST_METHOD'] == 'PUT'

    def is_delete_request(self):
        return self.environment['REQUEST_METHOD'] == 'DELETE'

    def is_patch_request(self):
        return self.environment['REQUEST_METHOD'] == 'PATCH'