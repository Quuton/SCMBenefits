from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib import auth

MAIN_PATH = 'main/'

# Create your views here.
def home(request):
    context = None

    return render(request, MAIN_PATH + 'index.html', context = context)

def announcements(request):
    context = None

    return render(request, MAIN_PATH + 'Announcements.html', context = context)

def benefits(request):
    context = None

    return render(request, MAIN_PATH + 'Benefits.html', context = context)

def login(request):
    context = None

    return render(request, MAIN_PATH + 'login.html', context = context)

def signup(request):
    context = None

    return render(request, MAIN_PATH + 'Signup.html', context = context)

def get_benefit(request, id: int = None):
    context = None

    return render(request, MAIN_PATH + 'index.html', context = context)

def get_announcement(request, id: int = None):
    context = None

    return render(request, MAIN_PATH + 'index.html', context = context)