from django.shortcuts import render
from django.http import HttpRequest

from chessboards.models import UserModel


async def index(request: HttpRequest):

    try:
        user = await UserModel.objects.aget(user_id=request.session.get("user_id"))
        return render(request, 'authorization/success_authorization.html')

    except UserModel.DoesNotExist:
        return render(request, 'authorization/authorization_form.html')
