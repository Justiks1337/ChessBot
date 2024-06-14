from rest_framework.serializers import Serializer, CharField, BooleanField, FileField, ModelSerializer
from chessboards.models import UserModel


class StartGameSerializer(Serializer):
    uuid = CharField(max_length=38)


class CheckInGameSerializer(Serializer):
    in_game = BooleanField()


class NewAuthorizeTokenSerializer(Serializer):
    success = BooleanField()
    token = CharField(max_length=38)


class DeleteAuthorizeTokenSerializer(Serializer):
    success = BooleanField()


class AuthorizeAttemptSerializer(Serializer):
    success = BooleanField()


class DashboardSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["user_id", "points", "username", "nickname"]
