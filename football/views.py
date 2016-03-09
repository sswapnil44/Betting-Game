import sys, os, django
sys.path.append(os.path.split(os.path.abspath(__file__))[0])
os.environ["DJANGO_SETTINGS_MODULE"] = "MakeABet.settings"
django.setup()

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from football.forms import BettingForm
from MakeABet.models import UserProfile
from football.models import Match
import datetime


def index(request):
    return render(request, 'football/index.html')


def league(request, league_name):
    league_name = league_name.replace("-"," ").title()
    league_dict = {'La Liga': 46,'Ligue 1': 47, 'Serie A': 49, 'Champions League': 36, 'Bundesliga': 48, 'Premier League': 2,}
    if league_name in league_dict:
        league_url = "-".join(league_name.lower().split())
        league_matches = Match.objects.filter(league=league_name)
        upcoming_matches = []

        for league_match in league_matches:
            match_time = datetime.datetime.fromtimestamp((league_match.time)/1000)
            if match_time > datetime.datetime.now():
                upcoming_matches.append([league_match, match_time])

        context = { 'league_name': league_name, 'upcoming_matches': upcoming_matches, 'league_url': league_url,}
        return render(request, 'football/league.html', context)
    else:
        return HttpResponseRedirect('/')


@login_required()
def match(request, league_name, match_id):

    match_data = Match.objects.get(match_id=match_id)
    match_time = datetime.datetime.fromtimestamp(match_data.time/1000)
    print("Before post method")
    if request.method == 'POST':
        print("post request received")
        betting_form = BettingForm(data=request.POST)
        if betting_form.is_valid():
            bet = betting_form.save(commit=False)
            bet.username = UserProfile.objects.get(user=request.user)
            try:
                bet.match_id = Match.objects.get(match_id=match_id)
            except:
                return HttpResponse('MatchID not found')
            try:
                bet.save()
            except:
                return HttpResponse("Bet already accepted for this match")
            return HttpResponse('Bet accepted')
        else:
            print(betting_form.errors)
    else:
        betting_form = BettingForm()

    context = {'match_data': match_data, 'match_time': match_time, 'betting_form': betting_form }

    return render(request, 'football/bet_page.html', context)
