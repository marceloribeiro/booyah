from lib.controllers.application_controller import ApplicationController
from lib.models.user import User
from lib.serializers.user_serializer import UserSerializer

class UsersController(ApplicationController):
    def index(self):
        if self.params.get('id'):
            users = users = User.where('id = ?', self.params['id'])
        elif self.params.get('first_name'):
            users = users = User.where('lower(first_name) like ?', f"%{self.params['first_name'].lower()}%")
        else:
            users = User.all()

        return self.render({ "users": list(map(lambda user: UserSerializer(user).to_dict(), users)) })

    def show(self):
        user = User.find(self.params['id'])
        return self.render({ "user": UserSerializer(user).to_dict() })