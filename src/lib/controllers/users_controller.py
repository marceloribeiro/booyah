from lib.controllers.application_controller import ApplicationController
from lib.models.user import User
from lib.serializers.user_serializer import UserSerializer

class UsersController(ApplicationController):
    def index(self):
        if self.params.get('id'):
            users = User.where('id = ?', self.params['id'])
        elif self.params.get('first_name'):
            users = User.where('lower(first_name) like ?', f"%{self.params['first_name'].lower()}%")
        else:
            users = User.all()

        return self.render({ "users": list(map(lambda user: UserSerializer(user).to_dict(), users)) })

    def show(self):
        user = User.find(self.params['id'])
        return self.render({ "user": UserSerializer(user).to_dict() })

    def create(self):
        user = User.create(self.user_params())
        return self.render({ "user": UserSerializer(user).to_dict() })

    def update(self):
        user = User.find(self.params['id'])

        if self.is_put_request():
            user.update(self.user_params())
        else:
            user.patch_update(self.user_params())

        return self.render({ "user": UserSerializer(user).to_dict() })

    def destroy(self):
        user = User.find(self.params['id'])
        deleted_id = user.destroy()
        return self.render({ "deleted": True, "deleted_id": deleted_id })

    def user_params(self):
        return { key: value for key, value in self.params['user'].items() if key in self.permitted_params() }

    def permitted_params(self):
        return ['first_name', 'last_name', 'email', 'password']