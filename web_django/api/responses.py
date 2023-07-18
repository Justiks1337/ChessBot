from typing import Optional


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


class AuthorizeAttemptResponse:
    def __init__(
            self,
            success: bool):

        self.success = success


class ChessboardMoveResponse:
    def __init__(self,
                 success: bool,
                 board: Optional[str],
                 message: Optional[str]):

        self.success = success
        self.board = board
        self.message = message
