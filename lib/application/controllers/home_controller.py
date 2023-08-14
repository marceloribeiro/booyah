from lib.application.controllers.application_controller import ApplicationController

class HomeController(ApplicationController):
    def index(self):
        return self.render('Home Controller, Index Action')

    def about(self):
        return self.render('Home Controller, About Action')