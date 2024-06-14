from django.shortcuts import render
from django.http import HttpRequest
from asgiref.sync import sync_to_async

from api.utils import in_database


async def index(request: HttpRequest):
    user_id = await (sync_to_async(request.session.get)("user_id"))

    if await in_database(user_id):
        return await (sync_to_async(render)(request, 'authorization/success_authorization.html'))
    return await (sync_to_async(render)(request, 'authorization/authorization_form.html'))


