from django.urls import path
from .views import index, board_view

urlpatterns = [
	path('games/<str:tag>/', index, name="chess_game"),
	path('boards/<str:tag>/', board_view)

]
