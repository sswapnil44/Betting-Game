from django import forms
from football.models import Bets


class BettingForm(forms.ModelForm):
    winner_prediction = forms.ChoiceField(choices=((0, 'Home Team'),(1, 'Away Team'),(2,'Draw')), required=False, )
    goal_difference = forms.IntegerField(min_value=0, max_value=30)
    home_goals_prediction = forms.IntegerField(min_value=0, max_value=30)
    away_goals_prediction = forms.IntegerField(min_value=0, max_value=30)

    class Meta:
        model = Bets
        fields = ('winner_prediction', 'goal_difference', 'home_goals_prediction', 'away_goals_prediction')