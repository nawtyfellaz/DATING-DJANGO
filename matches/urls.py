from django.urls import re_path, include
from .views import position_match_view, employer_match_view, location_match_view

app_name = 'matches'
urlpatterns = [
    re_path(r'^position/(?P<slug>[\w-]+)/$', position_match_view, name='position_match_view_url'),
    re_path(r'^employer/(?P<slug>[\w-]+)/$', employer_match_view, name='employer_match_view_url'),
    re_path(r'^location/(?P<slug>[\w-]+)/$', location_match_view, name='location_match_view_url'),
]