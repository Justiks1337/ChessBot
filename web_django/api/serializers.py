from rest_framework.serializers import Serializer, CharField, BooleanField, IntegerField


class StartGameSerializer(Serializer):
    uuid = CharField(max_length=38)


class NewAuthorizeTokenSerializer(Serializer):
    success = BooleanField()
    token = CharField(max_length=38)


class DeleteAuthorizeTokenSerializer(Serializer):
    success = BooleanField()


class AuthorizeAttemptSerializer(Serializer):
    success = BooleanField()


class ChessboardMoveSerializer(Serializer):
    success = BooleanField()
    board = CharField()
    message = CharField()
    time = IntegerField()


class ChessboardDrawSerializer(Serializer):
    success = BooleanField()


class ChessboardGiveUpSerializer(Serializer):
    success = BooleanField()
