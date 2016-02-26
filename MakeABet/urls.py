""" views
    2. Add a URL to urlpatterns:  uMakeABet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app importrl(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from MakeABet.views import *
from football.api_to_db import start_up
import multiprocessing

process = multiprocessing.Process(target=start_up)
process.start()

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^cricket/', include('cricket.urls')),
    url(r'^football/', include('football.urls')),
    url(r'^auth_key$', api_registration, name='registerapi'),
    url(r'^api/bets$', allBets, name='bets_info'),
    url(r'^api/matches$', allMatches, name='matches_info'),
    url(r'^leaderboard$', leaderboard, name='leaderboard'),
    url(r'^register$', register, name='register'),
    url(r'^login$', user_login, name='user_login'),
    url(r'^logout$', user_logout, name='user_logout'),
]
