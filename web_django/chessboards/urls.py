from django.urls import path
from .views import index

urlpatterns = [
	path('games/<str:tag>/', index, name="chess_game")
]
