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

