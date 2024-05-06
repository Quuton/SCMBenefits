from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('forbidden/', views.forbidden),
    path('not-found/', views.not_found),
    path('announcements/', views.announcements),
    path('benefits/', views.benefits),
    path('login/', views.login),
    path('logout/', views.logout),
    path('signup/', views.signup),
    path('get-benefit/<int:id>', views.get_benefit),
    path('get-announcement/<int:id>', views.get_announcement),
    path('delete-benefit/<int:id>', views.delete_benefit),
    path('delete-announcement/<int:id>', views.delete_announcement),
    path('edit-benefit/<int:id>', views.edit_benefit),
    path('edit-announcement/<int:id>', views.edit_announcement),
    path('add-benefit/', views.add_benefit),
    path('add-announcement/', views.add_announcement),
]