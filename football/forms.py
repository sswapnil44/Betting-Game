from django import forms
from django.contrib.auth.models import User
from football.models import Bets

class UserForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', )


class BettingForm(forms.ModelForm):
    winner_prediction = forms.ChoiceField(choices=((0, 'Home Team'),(1, 'Away Team'),(2,'Draw')), required=False, )
    goal_difference = forms.IntegerField(min_value=0, max_value=30)
    home_goals_prediction = forms.IntegerField(min_value=0, max_value=30)
    away_goals_prediction = forms.IntegerField(min_value=0, max_value=30)

    class Meta:
        model = Bets
        fields = ('winner_prediction', 'goal_difference', 'home_goals_prediction', 'away_goals_prediction')