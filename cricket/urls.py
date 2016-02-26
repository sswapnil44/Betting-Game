from django.conf.urls import url
from cricket.views import *

urlpatterns = [
    url(r'^$', index, name='cricket_index'),
]