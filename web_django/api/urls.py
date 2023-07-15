from django.urls import path

from .views import StartGameView, NewAuthorizeTokenView, DeleteAuthorizeTokenView


urlpatterns = [
    path('start_game', StartGameView().as_view()),
    path('new_token', NewAuthorizeTokenView().as_view()),
    path('delete_token', DeleteAuthorizeTokenView().as_view())
]