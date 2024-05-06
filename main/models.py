from django.db import models
from django.contrib.auth.models import User

class Benefit(models.Model):
    title = models.CharField(max_length = 50)
    summary = models.TextField(blank = True)
    description = models.TextField(blank = True)
    address_info = models.CharField(blank = True, max_length = 50)
    published_date = models.DateTimeField(auto_now = True)
    image = models.ImageField(upload_to='benefit_thumbnails',blank = True, default='placeholder.png')


class Announcement(models.Model):
    title = models.CharField(max_length = 50)
    summary = models.TextField(blank = True)
    description = models.TextField(blank = True)
    published_date = models.DateTimeField(auto_now = True)
    image = models.ImageField(upload_to='announcement_thumbnails',blank = True, default='placeholder.png')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone = models.CharField(max_length = 11)
    preferences_notify_benefits = models.BooleanField(default = True)
    preferences_notify_announcements = models.BooleanField(default = True)

