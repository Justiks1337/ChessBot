from django.db import models


class UserModel(models.Model):

    user_id = models.BigIntegerField(primary_key=True)
    games = models.IntegerField()
    points = models.IntegerField()
    nickname = models.TextField()
    username = models.TextField()
    ip_address = models.TextField(null=True)

    objects: models.Manager()

    class Meta:
        db_table = "users"
        managed = False


class GamesModel(models.Model):
    first_player = models.ForeignKey(UserModel, models.CASCADE, related_name='first_user')
    second_player = models.ForeignKey(UserModel, models.CASCADE, related_name='second_user')
    winner = models.ForeignKey(UserModel, models.CASCADE, related_name='win')

    objects: models.Manager()

    class Meta:
        db_table = "games"
        managed = False
