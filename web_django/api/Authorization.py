from uuid import uuid4

from authorization.core import fill_data


class Authorization:
    def __init__(self):
        self.authorization_tokens = {}

    def new_token(self, user_id: int):

        if user_id in list(self.authorization_tokens.keys()):
            return None

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

        return None

    async def successful_authorization(self, user_id: int):
        self.remove_token(user_id)

        return await fill_data(user_id)


main_authorization = Authorization()
