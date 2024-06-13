from django.db import models


class UserModel(models.Model):

    user_id = models.BigIntegerField(primary_key=True)
    games = models.IntegerField()
    points = models.IntegerField()
    nickname = models.TextField()
    username = models.TextField()
    ip_address = models.TextField(null=True)

    class Meta:
        db_table = "users"


class GamesModel(models.Model):
    first_player = models.ForeignKey(UserModel, models.CASCADE, related_name="first_player_id")
    second_player = models.ForeignKey(UserModel, models.CASCADE, related_name="second_player_id")
    winner = models.ForeignKey(UserModel, models.CASCADE, related_name="winner_id")
