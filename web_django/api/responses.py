class StartGameResponse:
    def __init__(self, uuid: str):
        self.uuid = uuid


class CheckInGameResponse:
    def __init__(self, in_game: bool):
        self.in_game = in_game


class NewAuthorizeTokenResponse:
    def __init__(self, success: bool, token: str):
        self.success = success
        self.token = token


class DeleteAuthorizeTokenResponse:
    def __init__(self, success):
        self.success = success


class AuthorizeAttemptResponse:
    def __init__(
            self,
            success: bool,
            message: str = "no message"):

        self.success = success
        self.message = message
