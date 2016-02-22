from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from football.forms import UserForm
from BetScore.models import Users
from django.contrib.auth import hashers
import time
from football.football_data import matchSelection, league_matches_list, all_match_updates

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
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
def register_api(request):
    user = Users()
    user.email = request.user.email
    user.auth_key = hashers.mask_hash(request.user.email + str(time.time()))
    try:
        user.save()
        return HttpResponse("test" + user.auth_key)
    except:
        return HttpResponse("Already registered")

#apiKey = open('api_key', 'r').read()
def league(request, league_name):
    league_name = league_name.replace("-"," ").title()
    league_dict = {'La Liga': 46,'Ligue 1': 47, 'Serei A': 160, 'Champions League': 36, 'Bundesliga': 48, 'English Premier League': 2 }
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

def match(request, league_name, match_id):
    print(match_id)
    print(league_name)
    print("gfhf")
    league_dict = {'La Liga': 46,'Ligue 1': 47, 'Serei A': 160, 'Champions League': 36, 'Bundesliga': 48, 'English Premier League': 2 }
    league_name = league_name.replace("-"," ").title()
    match_data = matchSelection(match_id)
    context = {'match_data': match_data, }
    return render(request, 'bet_page.html', context)