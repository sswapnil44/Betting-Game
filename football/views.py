import sys, os, django
sys.path.append(os.path.split(os.path.abspath(__file__))[0])
os.environ["DJANGO_SETTINGS_MODULE"] = "MakeABet.settings"
django.setup()

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from football.forms import UserForm, BettingForm
from football.models import UserProfile, Match, Bets
from rest_framework.authtoken.models import Token
from football.football_data import matchSelection, league_matches_list, all_match_updates
import simplejson

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = UserProfile()
            profile.user = user
            profile.points = 0
            profile.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    context = {'registered': registered, 'user_form':user_form}
    return render(request, 'register.html', context)

def user_login(request):
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                # valid and active account
                login(request,user)
                return HttpResponseRedirect('/')

            else:
                #inactive user account
                return HttpResponse('Your account is disabled')
        else:
            # wrong login details
            print("Invalid username, password combination")
            return HttpResponse('Invalid Login details provided')
    else:
        # for method other then POST
        return render(request, 'login.html')


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required()
def api_registration(request):
    try:
        token = Token.objects.create(user=request.user)
        return HttpResponse('Your auth_key: '+str(token.key))
    except:

        return HttpResponse('Your auth_key: '+str(Token.objects.get(user=request.user)))


def league(request, league_name):
    league_name = league_name.replace("-"," ").title()
    league_dict = {'La Liga': 46,'Ligue 1': 47, 'Serie A': 49, 'Champions League': 36, 'Bundesliga': 48, 'English Premier League': 2 }
    if league_name in league_dict:
        league_url = "-".join(league_name.lower().split())
        league_wise_match = all_match_updates()
        league_matches = league_matches_list(league_wise_match,league_dict[league_name])
        upcoming_matches = league_matches['upcomingMatches']
        print(league_matches)
        context = { 'league_name': league_name, 'upcoming_matches': upcoming_matches, 'league_url': league_url, }
        return render(request, 'league.html', context)
    else:
        return HttpResponseRedirect('/')

@login_required()
def match(request, league_name, match_id):
    league_dict = {'La Liga': 46,'Ligue 1': 47, 'Serie A': 49, 'Champions League': 36, 'Bundesliga': 48, 'English Premier League': 2 }
    league_name = league_name.replace("-"," ").title()
    match_data = matchSelection(match_id)

    if request.method == 'POST':
        print("post request received")
        betting_form = BettingForm(data=request.POST)
        if betting_form.is_valid():
            bet = betting_form.save(commit=False)
            bet.username = request.user
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


    context = {'match_data': match_data, 'betting_form': betting_form }

    return render(request, 'bet_page.html', context)



def allBets(request, type, auth_key):
    if auth_key == str(Token.objects.get(user=request.user)):
        try:
            betDetails = []
            bets = []

            type = type.split("=")

            if type[0]=='all':
                bets = Bets.objects.filter()

            elif type[0]=='username':
                bets = Bets.objects.filter(username__user__username=type[1])

            elif type[0]=='match_id':
                bets = Bets.objects.filter(match_id__match_id=int(type[1]))

            elif type[0]=='league_id':
                value = {1:'Premier League', 2:'La Liga', 3:'Serie A', 4:'Champions League', 5:'Bundesliga', 6:'Ligue 1'}
                bets = Bets.objects.filter(match_id__league=value[int(type[1])])

            res = {0:'homeTeam', 1:'awayTeam', 2:'draw'}
            for bet in bets:
                betDetails.append({'userDetails':{'username':bet.username.user.username,
                            'name':bet.username.user.first_name+" "+bet.username.user.last_name,
                            'email':bet.username.user.email, 'points':bet.username.points},
                                    'matchDetails':{'matchID':bet.match_id.match_id,
                            'startTime':bet.match_id.time, 'league':bet.match_id.league,
                            'homeTeam':bet.match_id.home_team, 'awayTeam':bet.match_id.away_team,
                            'homeTeamGoals':bet.match_id.home_team_goals, 'awayTeamGoals':bet.match_id.away_team_goals,
                            'outcome':bet.match_id.outcome},
                                     'predictions':{'winner': res[bet.winner_prediction], 'goalDifference':bet.goal_difference,
                            'homeTeamGoals':bet.home_goals_prediction, 'awayTeamGoals':bet.away_goals_prediction}})

            return HttpResponse(simplejson.dumps(betDetails))
        except:
            return HttpResponse('invalid url')
    else:
        return HttpResponse('Invalid auth_key, Register to get auth_key')
