from django.urls import path

from .views import (StartGameView,
                    NewAuthorizeTokenView,
                    DeleteAuthorizeTokenView,
                    authorization_attempt,
                    chessboard_move,
                    chessboard_draw,
                    chessboard_give_up)


urlpatterns = [
    path('start_game', StartGameView().as_view()),
    path('new_token', NewAuthorizeTokenView().as_view()),
    path('delete_token', DeleteAuthorizeTokenView().as_view()),
    path('authorize', authorization_attempt),
    path('chessboard_move', chessboard_move),
    path('chessboard_draw', chessboard_draw),
    path('chessboard_give_up', chessboard_give_up)

]