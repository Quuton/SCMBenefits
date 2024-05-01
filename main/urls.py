from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('announcements', views.announcements),
    path('benefits', views.benefits),
    path('login', views.login),
    path('signup', views.signup),
    path('get-benefit', views.get_benefit),
    path('get-announcement', views.get_announcement),
]