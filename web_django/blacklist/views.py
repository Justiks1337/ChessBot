from adrf.decorators import api_view
from django.db import models
from rest_framework.request import Request
from rest_framework.response import Response
from asgiref.sync import sync_to_async

from blacklist.models import BlacklistModel
from chessboards.models import UserModel
from api.utils import authorization


@api_view(["GET"])
@authorization
async def in_blacklist(request: Request):
    try:
        user_id = await (sync_to_async(request.query_params.get)("user_id"))

        await BlacklistModel.objects.aget(blacklist_user_id=await UserModel.objects.aget(user_id=user_id))

    except (UserModel.DoesNotExist, BlacklistModel.DoesNotExist):
        return Response({"in_blacklist": True})


@api_view(["POST"])
@authorization
async def add_to_blacklist(request: Request):
    try:
        user_id = await (sync_to_async(request.query_params.get)("user_id"))

        user = BlacklistModel(blacklist_user_id=await UserModel.objects.aget(user_id=user_id))
        await user.asave()

        return Response({"status": 200})
    except (UserModel.DoesNotExist, BlacklistModel.DoesNotExist):
        return Response({"status": 404})


@api_view(["POST"])
@authorization
async def remove_from_blacklist(request: Request):
    try:
        user_id = await (sync_to_async(request.query_params.get)("user_id"))

        user = await BlacklistModel.objects.all().afilter(
            blacklist_user_id=await UserModel.objects.aget(user_id=user_id))
        await user.adelete()

        return Response({"status": 200})

    except (UserModel.DoesNotExist, BlacklistModel.DoesNotExist):
        return Response({"status": 404})

