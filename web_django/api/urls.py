from django.urls import path

from api.views import (
    start_game,
    check_in_game,
    new_authorize_token,
    delete_authorize_token,
    authorization_attempt,
    check_timer)

urlpatterns = [
    path('check_in_game', check_in_game),
    path('new_token', new_authorize_token),
    path('delete_token', delete_authorize_token),
    path('authorize', authorization_attempt),
    path('start_game', start_game),
    path('check_timer', check_timer),
]
