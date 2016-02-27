from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from football.forms import UserForm, BettingForm
from football.models import UserProfile, Match, Bets
from rest_framework.authtoken.models import Token
import simplejson

def home(request):
    context_dict = dict()
    if not str(request.user) == "AnonymousUser":
        user_profile = UserProfile.objects.get(user=request.user)
        context_dict = {'points': user_profile.points}

    return render(request, 'home.html', context_dict)

@login_required()
def api_registration(request):
    try:
        token = Token.objects.create(user=request.user)
        return HttpResponse('Your auth_key: '+str(token.key))
    except:

        return HttpResponse('Your auth_key: '+str(Token.objects.get(user=request.user)))

def allBets(request):
    api_key = request.GET.get('api_key', None)
    if api_key == str(Token.objects.get(key=api_key)):
        username = request.GET.get('username',None)
        match_id = request.GET.get('match_id',None)
        league_id = request.GET.get('league_id',None)

        bets = Bets.objects.filter()

        if username is not None:
            bets = bets.filter(username__user__username=username)
        if match_id is not None:
            bets = bets.filter(match_id__match_id =int(match_id))
        if league_id is not None:
            value = {1:'Premier League', 2:'La Liga', 3:'Serie A', 4:'Champions League', 5:'Bundesliga', 6:'Ligue 1'}
            bets = bets.filter(match_id__league=value[int(league_id)])


        res = {0:'homeTeam', 1:'awayTeam', 2:'draw'}
        betDetails = []
        for bet in bets:
            betDetails.append({'userDetails':{'username':bet.username.user.username,
                        'name':bet.username.user.first_name+" "+bet.username.user.last_name,
                        'points':bet.username.points},
                                'matchDetails':{'matchID':bet.match_id.match_id,
                        'startTime':bet.match_id.time, 'league':bet.match_id.league,
                        'homeTeam':bet.match_id.home_team, 'awayTeam':bet.match_id.away_team,
                        'homeTeamGoals':bet.match_id.home_team_goals, 'awayTeamGoals':bet.match_id.away_team_goals,
                        'outcome':bet.match_id.outcome},
                                 'predictions':{'winner': res[bet.winner_prediction], 'goalDifference':bet.goal_difference,
                        'homeTeamGoals':bet.home_goals_prediction, 'awayTeamGoals':bet.away_goals_prediction}})


        return HttpResponse(simplejson.dumps(betDetails))
    else:
        return HttpResponse('Invalid auth_key, Register to get auth_key', status=403)

def allMatches(request):
    api_key = request.GET.get('api_key', None)

    if api_key == str(Token.objects.get(key=api_key)):
        match_id = request.GET.get('match_id',None)
        league_id = request.GET.get('league_id',None)

        matches = Match.objects.filter()

        if match_id is not None:
            matches = matches.filter(match_id =int(match_id))
        if league_id is not None:
            value = {1:'Premier League', 2:'La Liga', 3:'Serie A', 4:'Champions League', 5:'Bundesliga', 6:'Ligue 1'}
            matches = matches.filter(match_id__league=value[int(league_id)])


        res = {0:'homeTeam', 1:'awayTeam', 2:'draw'}
        matchDetails = []
        for match in matches:
            matchDetails.append({'matchID':match.match_id,
                        'startTime':match.time, 'league':match.league,
                        'homeTeam':match.home_team, 'awayTeam':match.away_team,
                        'homeTeamGoals':match.home_team_goals, 'awayTeamGoals':match.away_team_goals,
                        'outcome':match.outcome})

        return HttpResponse(simplejson.dumps(matchDetails))
    else:
        return HttpResponse('Invalid auth_key, Register to get auth_key', status=403)

@login_required()
def leaderboard(request):
    user_profiles = UserProfile.objects.all().order_by('points').reverse()
    context_dict = {'user_profiles': user_profiles, }
    return render(request, 'leaderboard.html', context_dict)

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

