from lib.controllers.application_controller import ApplicationController
from lib.models.user import User
from lib.serializers.user_serializer import UserSerializer

class UsersController(ApplicationController):
    def index(self):
        users = User.all()
        return self.render({ "users": list(map(lambda user: UserSerializer(user).to_dict(), users)) })

    def show(self):
        user = User.find(self.params['id'])
        return self.render({ "user": UserSerializer(user).to_dict() })