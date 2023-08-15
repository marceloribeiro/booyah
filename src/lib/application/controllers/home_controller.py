from lib.application.controllers.application_controller import ApplicationController

class HomeController(ApplicationController):
    def index(self):
        return self.render({'text': 'Home Controller, Index Action'})

    def about(self):
        return self.render({'text': 'Home Controller, About Action'})

    def status(self):
        return self.render({'text': 'Home Controller, Status Action'})

    def plain(self):
        return self.render({'text': 'Home Controller, Plain Action'})