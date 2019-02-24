from django.urls import path, re_path

from .views import (
        AccountHomeView, 
        AccountEmailActivateView,
        UserDetailUpdateView,
        )
app_name = 'account'
urlpatterns = [
    path('', AccountHomeView.as_view(), name='home'),
    #re_path(r'^(?P<short_name>[\w.@+-]+)/$', AccountHomeView.as_view(), name='home'), to use the username or short name in the url convention
#     path('userdetail/', UserDetailUpdateView.as_view(), name='user-update'),
    path('userdetail/', UserDetailUpdateView, name='user-update'),
    re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', 
            AccountEmailActivateView.as_view(), 
            name='email-activate'),
    path('email/resend-activation/', 
            AccountEmailActivateView.as_view(), 
            name='resend-activation'),
]

