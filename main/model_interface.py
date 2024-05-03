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

def save_benefit(data:dict, id = None):
    temp = None
    if id != None:
        temp = Benefit.objects.get(id = id)
        temp.title = data.get('title')
        temp.summary = data.get('summary')
        temp.description = data.get('description')
        temp.address_info = data.get('address_info')
        temp.published_date = data.get('published_date')
        temp.image = data.get('image')
        temp.save()

    else:
        temp = Benefit(
            title = data.get('title'),
            summary = data.get('summary'),
            description = data.get('description'),
            address_info = data.get('address_info'),
            published_date = data.get('published_date'),
            image = data.get('image')
        )
        temp.save()

    return temp

def get_all_announcement(max_posts = 999):
    return Announcement.objects.order_by('-published_date')[:max_posts]

def get_announcement(id):
    return Announcement.objects.get(id = id)

def save_announcement(data:dict, id = None):
    temp = None
    if id != None:
        temp = Announcement.objects.get(id = id)
        temp.title = data.get('title')
        temp.summary = data.get('summary')
        temp.description = data.get('description')
        temp.published_date = data.get('published_date')
        temp.image = data.get('image')
        temp.save()

    else:
        temp = Announcement(
            title = data.get('title'),
            summary = data.get('summary'),
            description = data.get('description'),
            published_date = data.get('published_date'),
            image = data.get('image')
        )
        temp.save()
        
    return temp

def delete_benefit(id):
    Benefit.objects.filter(id = id).delete()

def delete_announcement(id):
    Announcement.objects.filter(id = id).delete()