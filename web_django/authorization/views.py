from django.shortcuts import render
from django.http import HttpRequest
from .core import get_session_key

from database_tools.Connection import connect

# Create your views here.


async def index(request: HttpRequest):

    try:

        session_key = await get_session_key(request)

        data = await (await connect.request(
            "SELECT user_id, games, points, nickname, username FROM users WHERE session_id = ?", (session_key, ))
                    ).fetchone()

        try:
            open(f"web_django/static/avatars/{data[0]}.png")

            avatar_path = f"static/avatars/{data[0]}.png"

        except FileNotFoundError:
            avatar_path = "static/avatars/unknown_user.png"

        return render(request, 'authorization/profile.html', {
            "avatar_path": avatar_path,
            "user_id": data[0],
            "games": data[1],
            "points": data[2],
            "nickname": data[3],
            "username": data[4]})

    except TypeError:

        if request.COOKIES == {}:
            request.session['cookie_init'] = 'true'

        return render(request, 'authorization/authorization_form.html')
