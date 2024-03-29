from django.urls import path
from chessboards.views import game_view

urlpatterns = [
	path('games/<str:tag>/', game_view, name="chess_game")
]
