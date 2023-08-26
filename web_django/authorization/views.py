from django.shortcuts import render
from django.http import HttpRequest
from .core import get_session_key

from database_tools.Connection import connect

# Create your views here.


async def index(request: HttpRequest):

    session_key = await get_session_key(request)

    user = await (await connect.request("SELECT user_id FROM users WHERE session_id = ?", (session_key, ))).fetchone()

    if user:
        return render(request, 'authorization/success_authorization.html')

    if request.COOKIES == {}:
        request.session['cookie_init'] = 'true'

    return render(request, 'authorization/authorization_form.html')
