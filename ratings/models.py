from django.db import models


class Person(models.Model):
    username = models.CharField(max_length=200, unique=True)
    rating = models.IntegerField(null=True, blank=True)


class Game(models.Model):
    winner = models.ForeignKey(Person, related_name='winner_username')
    loser = models.ForeignKey(Person, related_name='loser_username')
    win_score = models.IntegerField()
    lose_score = models.IntegerField()
    game_date = models.DateTimeField('game played')
