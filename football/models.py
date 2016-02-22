from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    #Links UserProfile to User model
    user = models.OneToOneField(User)

    points = models.IntegerField(default=0, )

    def __unicode__(self):
        return self.user.username

class Match(models.Model):
    match_no = models.IntegerField(primary_key=True,unique=True)
    match_id = models.IntegerField()
    time = models.TimeField()
    league = models.TextField(max_length=100)
    home_team = models.TextField(max_length=100)
    away_team = models.TextField(max_length=100)
    home_team_goals = models.IntegerField(default=None)
    away_team_goals = models.IntegerField(default=None)
    penalties = models.BooleanField(default=False)
    home_penalty_goals = models.IntegerField(default=None)
    away_penalty_goals = models.IntegerField(default=None)

    def __unicode__(self):
        return self.home_team + "    " + self.home_team_goals + "  Vs   " + self.away_team_goals + "     " + self.away_team
