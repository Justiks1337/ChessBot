from django.shortcuts import render
from django.http import HttpRequest
from .core import get_session_key

from chessboards.models import UserModel


async def index(request: HttpRequest):

    session_key = await get_session_key(request)

    try:
        user = await UserModel.objects.aget(session_id=session_key)
        return render(request, 'authorization/success_authorization.html')

    except UserModel.DoesNotExist:
        if request.COOKIES == {}:
            request.session['cookie_init'] = 'true'
        return render(request, 'authorization/authorization_form.html')
