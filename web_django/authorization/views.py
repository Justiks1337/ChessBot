from django.shortcuts import render
from django.http import HttpRequest
from asgiref.sync import sync_to_async

from chessboards.models import UserModel


async def index(request: HttpRequest):

    try:
        await UserModel.objects.aget(user_id=await sync_to_async(request.session.get)("user_id"))
        return await sync_to_async(render)(request, 'authorization/success_authorization.html')

    except UserModel.DoesNotExist:
        return await sync_to_async(render)(request, 'authorization/authorization_form.html')
