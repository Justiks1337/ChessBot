from django.urls import path

from api.views import (
    start_game,
    check_in_game,
    new_authorize_token,
    authorization_attempt,
    check_timer,
    download_avatar,
    in_database_api,
    dashboard,
    UserInfo)

urlpatterns = [
    path('check_in_game', check_in_game),
    path('new_token', new_authorize_token),
    path('authorize', authorization_attempt),
    path('start_game', start_game),
    path('check_timer', check_timer),
    path('add_avatar', download_avatar),
    path('in_database', in_database_api),
    path('dashboard', dashboard),
    path('profile/<int:user_id>/', UserInfo.as_view())
]
