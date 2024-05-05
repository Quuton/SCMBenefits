from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib import auth
from . import model_interface as mi

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
    context = {'announcements':mi.get_all_announcement(4),
               'benefits':mi.get_all_benefit(4)}
    
    return render(request, MAIN_PATH + TEMPLATES['home'], context = context)

def forbidden(request):
    return render(request, "forbidden")

def announcements(request):
    context = {'annnouncements':mi.get_all_announcement()}

    return render(request, MAIN_PATH + TEMPLATES['announcements'], context = context)

def benefits(request):  
    context = {'benefits':mi.get_all_benefit()}
    return render(request, MAIN_PATH + TEMPLATES['benefits'], context = context)

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, MAIN_PATH + TEMPLATES['login'], context = {'auth_status':'Credentials do not match any account!'})

    else:
        return render(request, MAIN_PATH + TEMPLATES['login'])

def logout(request):
    auth.logout(request)
    return redirect('/')

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            phone = request.POST['phone']
            mi.register_user(username, first_name, last_name, password, phone, email)
        else:
            return render(request, MAIN_PATH + TEMPLATES['signup'])

def get_benefit(request, id: int = None):
    context = {'benefit':mi.get_benefit(id)}
    return render(request, MAIN_PATH + TEMPLATES['benefit'], context = context)

def get_announcement(request, id: int = None):
    context = {'announcement':mi.get_announcement(id)}
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

    if (request.method == "POST" and id != None):
        title = request.POST['title']
        summary = request.POST['summary']
        description = request.POST['description']
        address_info = request.POST['address_info']
        published_date = request.POST['published_date']

        image = None
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
        
        notify_subscribers = (request.POST.getlist('notify_subscribers') != [])

        # TODO add sms notification shit here xd

        return redirect('/')
    else:
        return render(request, MAIN_PATH + TEMPLATES['benefit_add_form'])

    

def add_announcement(request):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/forbidden')

    if (request.method == "POST" and id != None):
        title = request.POST['title']
        summary = request.POST['summary']
        description = request.POST['description']
        address_info = request.POST['address_info']
        published_date = request.POST['published_date']

        image = None
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
        
        # TODO

        return redirect('/')
    else:
        return render(request, MAIN_PATH + TEMPLATES['announcement_add_form'])
