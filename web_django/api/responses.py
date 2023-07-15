class StartGameResponse:
    def __init__(self, uuid: str):
        self.uuid = uuid


class NewAuthorizeTokenResponse:
    def __init__(self, success: bool, token: str):
        self.success = success
        self.token = token


class DeleteAuthorizeTokenResponse:
    def __init__(self, success):
        self.success = success
