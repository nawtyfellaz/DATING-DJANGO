"""dating URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, re_path, include

#ACCOUNT VIEW IMPORTS
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, RedirectView
from accounts.views import LoginView, RegisterView#, StaffRegisterView

#Project Main Views (home, about, contact)
from .views import index

# from questions.views import single, home
# from newsletter.views import contact
# from likes.views import like_user
# from profiles.views import profile_edit, profile_user, profile_view, job_add, jobs_edit

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home, Contact & About urls
    path('', index, name='home'),

    #ACCOUNT LINKS AND PASSWORD(LOGIN & LOGOUT)
    path('accounts/', RedirectView.as_view(url='/account')),
    path('account/', include("accounts.urls", namespace='account')),
    path('accounts/', include("accounts.passwords.urls")),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    #APPS URLS
    # path('', 'dashboard.views.home', name='home'),
    # re_path(r'^question/(?P<id>\d+)/$', single, name='question_single'),
    # path('question/', home, name='question_home'),
    # path('contact/', contact, name='contact'),
    # path('matches/', include('matches.urls', namespace='matches')),
    # re_path(r'^like/(?P<id>\d+)/$', like_user, name='like_user'),
    # path('profile/edit/', profile_edit, name='profile_edit'),
    # re_path(r'^profile/(?P<username>[\w.@+-]+)/$', profile_view, name='profile'),
    # path('profile/jobs/add/', job_add, name='job_add'),
    # path('profile/jobs/edit/', jobs_edit, name='jobs_edit'),
    # path('profile/', profile_user, name='profile_user'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)