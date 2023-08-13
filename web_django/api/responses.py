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
                 board: Optional[str] = None,
                 message: Optional[str] = None,
                 time: Optional[int] = None):

        self.success = success
        self.board = board
        self.message = message
        self.time = time


class ChessboardDrawResponse:
    def __init__(self, success: bool):

        self.success = success


class ChessboardGiveUpResponse:
    def __init__(self, success: bool):

        self.success = success
