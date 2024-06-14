from django.db import models

from chessboards.models import UserModel


class BlacklistModel(models.Model):
    blacklist_user_id = models.ForeignKey(UserModel, models.CASCADE, related_name="blacklist_user_id")
