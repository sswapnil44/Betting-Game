from django.db import models
from MakeABet.models import UserProfile


class Match(models.Model):
    match_id = models.IntegerField(primary_key=True)
    time = models.FloatField(max_length=20, blank=False)
    league = models.TextField(max_length=100)
    home_team = models.TextField(max_length=100)
    away_team = models.TextField(max_length=100)
    home_team_goals = models.IntegerField(blank=True, null=True)
    away_team_goals = models.IntegerField(blank=True, null=True)
    outcome = models.TextField(null=True, default=None)

    def __str__(self):
        a = str(self.match_id) + " - " + self.home_team + " Vs " + self.away_team
        return a


class Bets(models.Model):
    match = models.ForeignKey(Match)
    user_profile = models.ForeignKey(UserProfile)
    winner_prediction = models.SmallIntegerField(blank=True, null=True)
    goal_difference = models.SmallIntegerField(blank=True, null=True)
    home_goals_prediction = models.SmallIntegerField(blank=True, null=True)
    away_goals_prediction = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('match', 'user_profile')

    def __str__(self):
        a = "For match " + str(self.match.match_id) + " by " + str(self.username.user.username)
        return a
