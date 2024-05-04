from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib import auth
import model_interface as mi

MAIN_PATH = 'main/'
TEMPLATES = {'home':'index.html',
            'announcements':'Announcements.html',
            'benefits':'Benefits.html',
            'login':'Login.html',
            'signup':'Signup.html',
            'announcement':'',
            'benefit':'',
            'benefit_add_form':'',
            'announcement_add_form':'',
            'benefit_edit_form':'',
            'announcement_edit_form':''
}


# Create your views here.
def home(request):
    context = None

    return render(request, MAIN_PATH + TEMPLATES['home'], context = context)

def forbidden(request):
    return render(request, "forbidden")

def announcements(request):
    context = mi.get_all_announcement()

    return render(request, MAIN_PATH + TEMPLATES['announcements'], context = context)

def benefits(request):  
    context = mi.get_all_benefit

    return render(request, MAIN_PATH + TEMPLATES['benefits'], context = context)

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, MAIN_PATH + TEMPLATES['login'])

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, MAIN_PATH + TEMPLATES['signup'])

def get_benefit(request, id: int = None):
    context = mi.get_benefit(id)

    return render(request, MAIN_PATH + TEMPLATES['benefit'], context = context)

def get_announcement(request, id: int = None):
    context = mi.get_announcement(id)

    return render(request, MAIN_PATH + TEMPLATES['announcement'], context = context)

def delete_benefit(request, id: int = None):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/forbidden')

    # I really HATE this, i would want the user to send a DELETE request, but its not possible with vanilla html
    if (request.method == "GET" and id != None):
        mi.delete_benefit(id)
        return redirect('/benefits')
    else:   
        return redirect('/')

def delete_announcement(request, id: int = None):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/forbidden')

    if (request.method == "GET" and id != None):
        mi.delete_announcement(id)
        return redirect('/announcements')
    else:
        return redirect('/')

    

def edit_benefit(request, id: int = None):
    context = None

    return render(request, MAIN_PATH + 'index.html', context = context)

def edit_announcement(request, id: int = None):
    context = None

    return render(request, MAIN_PATH + 'index.html', context = context)

def add_benefit(request):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/forbidden')

    return render(request, MAIN_PATH + 'index.html')

def add_announcement(request):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/forbidden')

    if (request.method == "POST" and id != None):
        # mi.delete_announcement(id)
        # return redirect('/announcements')
        pass
    else:
        return redirect('/')

    return render(request, MAIN_PATH + 'index.html')