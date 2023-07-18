from uuid import uuid4

from exceptions.UnsuccessfulAuthorization import UnsuccessfulAuthorization
from exceptions.DuplicateAuthorizationTokenError import DuplicateAuthorizationTokenError
from web_django.authorization.core import fill_data


class Authorization:
    def __init__(self):
        self.authorization_tokens = {}

    def new_token(self, user_id: int):

        if user_id in list(self.authorization_tokens.keys()):
            raise DuplicateAuthorizationTokenError()

        token = str(uuid4())

        self.authorization_tokens[user_id] = token

        return token

    def remove_token(self, user_id: int):
        del self.authorization_tokens[user_id]

    async def authorization(self, token: str):

        for user_id in list(self.authorization_tokens.keys()):

            if self.authorization_tokens[user_id] == token:
                await self.successful_authorization(user_id)
                return user_id

        self.unsuccessful_authorization()

    async def successful_authorization(self, user_id: int):
        self.remove_token(user_id)

        await fill_data(user_id)

    def unsuccessful_authorization(self):
        raise UnsuccessfulAuthorization()


main_authorization = Authorization()
