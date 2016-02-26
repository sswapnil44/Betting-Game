from django.conf.urls import url
from football.views import *


urlpatterns = [
    url(r'^$', index, name='football_index'),
    url(r'^(?P<league_name>[\w\-]+)$', league, name='league'),
    url(r'^(?P<league_name>[\w\-]+)/(?P<match_id>[\d]+)$', match, name='match'),
]