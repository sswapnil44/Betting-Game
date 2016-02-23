from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from football.forms import UserForm, BettingForm
from football.models import UserProfile, Match
from rest_framework.authtoken.models import Token
from football.football_data import matchSelection, league_matches_list, all_match_updates

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
        return HttpResponse(token.key)
    except:
        return HttpResponse(Token.objects.get(user=request.user))

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
