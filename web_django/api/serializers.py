from rest_framework.serializers import Serializer, CharField, BooleanField


class StartGameSerializer(Serializer):
    uuid = CharField(max_length=38)


class NewAuthorizeTokenSerializer(Serializer):
    success = BooleanField()
    token = CharField(max_length=38)


class DeleteAuthorizeTokenSerializer(Serializer):
    success = BooleanField()


class AuthorizeAttemptSerializer(Serializer):
    success = BooleanField()
