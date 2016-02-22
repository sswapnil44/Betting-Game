from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    #Links UserProfile to User model
    user = models.OneToOneField(User)

    points = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

class Match(models.Model):
    match_id = models.IntegerField(primary_key=True)
    time = models.TimeField()
    league = models.TextField(max_length=100)
    home_team = models.TextField(max_length=100)
    away_team = models.TextField(max_length=100)
    home_team_goals = models.IntegerField(blank=True, null=True)
    away_team_goals = models.IntegerField(blank=True, null=True)
    penalties = models.BooleanField(default=False)
    home_penalty_goals = models.IntegerField(blank=True, null=True)
    away_penalty_goals = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.home_team + "    " + self.home_team_goals + "  Vs   " + self.away_team_goals + "     " + self.away_team

class Bets(models.Model):
    match_id = models.ForeignKey(Match)
    username = models.ForeignKey(User)
    winner_prediction = models.SmallIntegerField(blank=True, null=True)
    goal_difference = models.SmallIntegerField(blank=True, null=True)
    home_goals_prediction = models.SmallIntegerField(blank=True, null=True)
    away_goals_prediction = models.SmallIntegerField(blank=True, null=True)

    def __unicode__(self):
        return "Prediction for match no." + str(self.match_no)+" by" + self.username

    class Meta:
        unique_together = ('match_id', 'username')