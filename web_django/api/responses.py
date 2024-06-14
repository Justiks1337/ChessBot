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


class DashboardResponse:
    def __init__(self,
                 user_id, points, username, nickname):
        self.user_id = user_id
        self.points = points
        self.username = username
        self.nickname = nickname




