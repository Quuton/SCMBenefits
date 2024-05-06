from .models import *
import random
import itertools as it
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.models import Avg

def get_all_benefit(max_posts = 999):
    return Benefit.objects.order_by('-published_date')[:max_posts]

def get_benefit(id):
    return Benefit.objects.get(id = id)

def save_benefit(title, summary, description, address_info, published_date, image, id = None):
    temp = None
    if id != None:
        temp = Benefit.objects.get(id = id)
        temp.title = title
        temp.summary = summary
        temp.description = description
        temp.address_info = address_info
        temp.published_date = published_date
        temp.image = image
        temp.save()

    else:
        temp = Benefit(
            title = title,
            summary = summary,
            description = description,
            address_info = address_info,
            published_date = published_date,
            image = image
        )
        temp.save()

    return temp

def get_all_announcement(max_posts = 999):
    return Announcement.objects.order_by('-published_date')[:max_posts]

def get_announcement(id):
    return Announcement.objects.get(id = id)

def save_announcement(title, summary, description, published_date, image, id = None):
    temp = None
    if id != None:
        temp = Announcement.objects.get(id = id)
        temp.title = title
        temp.summary = summary
        temp.description = description
        temp.published_date = published_date
        temp.image = image
        temp.save()

    else:
        temp = Announcement(
            title = title,
            summary = summary,
            description = description,
            published_date = published_date,
            image = image
        )
        temp.save()
        
    return temp

def delete_benefit(id):
    Benefit.objects.filter(id = id).delete()

def delete_announcement(id):
    Announcement.objects.filter(id = id).delete()

def register_user(username:str, first_name:str, last_name:str, password:str, phone:str, email:str = None):
    user = User.objects.create_user(username = username, email = email, password = password, first_name = first_name, last_name = last_name)
    group = Group.objects.get(name='User')
    user.groups.add(group)
    profile = UserProfile(user = user, phone = phone)
    profile.save()

def get_phone_list_benefits():
    return [i.phone for i in UserProfile.objects.filter(preferences_notify_benefits = True)]

def get_phone_list_announcements():
    return [i.phone for i in UserProfile.objects.filter(preferences_notify_announcements = True)]

def check_benefit_exists(id:int):
    return Benefit.objects.filter(id = id).exists()

def check_announcement_exists(id:int):
    return Announcement.objects.filter(id = id).exists()