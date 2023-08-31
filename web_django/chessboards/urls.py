from django.urls import path
from .views import game_view, board_view

urlpatterns = [
	path('games/<str:tag>/', game_view, name="chess_game"),
	path('boards/<str:tag>/', board_view)

]
