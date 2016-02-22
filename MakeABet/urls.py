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
from django.conf.urls import url
from django.contrib import admin
from . import views
from football.views import *
from MakeABet.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^register/$', register, name='register'),
    url(r'^login/$', user_login, name='user_login'),
    url(r'^logout/$', user_logout, name='user_logout'),
    url(r'^(?P<league_name>[\w\-]+)$', league, name='league'),
    url(r'^(?P<league_name>[\w\-]+)/(?P<match_id>[\d]+)$', match, name='match'),
    url(r'/register/api', register_api, name='apireg'),
]
