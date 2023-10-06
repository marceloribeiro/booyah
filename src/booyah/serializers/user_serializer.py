from booyah.serializers.application_serializer import ApplicationSerializer

class UserSerializer(ApplicationSerializer):
    def to_dict(self):
        to_return = super().to_dict()
        return to_return

    def to_json(self):
        to_return = super().to_json()
        return to_return