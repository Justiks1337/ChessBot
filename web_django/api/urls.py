from django.urls import path

from .views import (check_in_game,
                    new_authorize_token,
                    delete_authorize_token,
                    authorization_attempt)


urlpatterns = [
    path('check_in_game', check_in_game),
    path('new_token', new_authorize_token),
    path('delete_token', delete_authorize_token),
    path('authorize', authorization_attempt)
]
