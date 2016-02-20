from django.db import models
from django.contrib.auth.models import User

class Match(models.Model):
    match_id = models.IntegerField(primary_key=True,unique=True)
    time = models.TimeField()
    league = models.TextField(max_length=100)
    home_team = models.TextField(max_length=100)
    away_team = models.TextField(max_length=100)
    home_team_goals = models.IntegerField(default=None)
    away_team_goals = models.IntegerField(default=None)
    penalties = models.BooleanField(default=False)
    home_penalty_goals = models.IntegerField(default=None)
    away_penalty_goals = models.IntegerField(default=None)

