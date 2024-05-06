from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib import auth
from . import model_interface as mi
from .utility import messaging
import asyncio
from .utility import config
import threading
MAIN_PATH = 'main/'
TEMPLATES = {'home':'index.html',
            'announcements':'announcements.html',
            'benefits':'benefits.html',
            'login':'login.html',
            'signup':'signup.html',
            'announcement':'announcement.html',
            'benefit':'benefit.html',
            'benefit_add_form':'benefit_add_form.html',
            'announcement_add_form':'announcement_add_form.html',
            'benefit_edit_form':'benefit_edit_form.html',
            'announcement_edit_form':'announcement_edit_form.html'
}


# Create your views here.
def home(request):
    context = {'announcements':mi.get_all_announcement(4),
               'benefits':mi.get_all_benefit(4)}
    
    return render(request, MAIN_PATH + TEMPLATES['home'], context = context)

def forbidden(request):
    return render(request, "forbidden")

def not_found(request):
    return render(request, "Not found 404 :(")

def announcements(request):
    context = {'announcements':mi.get_all_announcement(10)}

    return render(request, MAIN_PATH + TEMPLATES['announcements'], context = context)

def benefits(request):  
    context = {'benefits':mi.get_all_benefit(10)
            }
    
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
            return redirect('/login/')
        else:
            return render(request, MAIN_PATH + TEMPLATES['signup'])

def get_benefit(request, id: int = None):
    context = {'benefit':mi.get_benefit(id),
               'gmaps_api_key':config.GMAPS_EMBED_API_KEY}
    
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

def edit_benefit(request, id: int):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/forbidden')
    
    if (id == None or not mi.check_benefit_exists(id)):
        return redirect('/not-found')
    
    temp_benefit = mi.get_benefit(id)

    if (request.method == "POST"):
        title = request.POST['title']
        summary = request.POST['summary']
        description = request.POST['description']
        address_info = request.POST['address_info']

        image = temp_benefit.image
        if request.FILES.get('thumbnail') != None:
            image = request.FILES.get('thumbnail')

        mi.save_benefit(title, summary, description, address_info, image, id)
        return redirect(f'/get-benefit/{id}')
    else:
        context = {'benefit':mi.get_benefit(id),
                    'id':id
                }
        return render(request, MAIN_PATH + TEMPLATES['benefit_edit_form'], context = context)

def edit_announcement(request, id:int):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/forbidden')
    
    if (id == None or not mi.check_announcement_exists(id)):
        return redirect('/not-found')
    
    temp_announcement = mi.get_announcement(id)

    if (request.method == "POST"):
        title = request.POST['title']
        summary = request.POST['summary']
        description = request.POST['description']

        image = temp_announcement.image
        if request.FILES.get('thumbnail') != None:
            image = request.FILES.get('thumbnail')

        mi.save_announcement(title, summary, description, image, id)
        return redirect(f'/get-announcement/{id}')
    else:
        context = {'announcement':mi.get_announcement(id),
                    'id':id
                }
        return render(request, MAIN_PATH + TEMPLATES['announcement_edit_form'], context = context)

def add_benefit(request):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/forbidden')

    if (request.method == "POST"):
        title = request.POST['title']
        summary = request.POST['summary']
        description = request.POST['description']
        address_info = request.POST['address_info']

        image = None
        if request.FILES.get('thumbnail') != None:
            image = request.FILES.get('thumbnail')

        mi.save_benefit(title, summary, description, address_info, image)
        
        if (request.POST.getlist('notify_subscribers') != []):
            SMS_MESSAGE = f"New Benefit!: {title}\n{summary}\n=====================\nDetails:\n{description}"
            thread = threading.Thread(target = messaging.send_batch_sms(SMS_MESSAGE, [messaging.format_local_number_philippines(i) for i in mi.get_phone_list_benefits()]), name = 'thread')
            thread.start()                       
            # asyncio.create_task(messaging.send_batch_sms(f"{title}\n{summary}", [messaging.format_local_number_philippines(i) for i in mi.get_phone_list_benefits()]))

        return redirect('/benefits/')
    else:
        return render(request, MAIN_PATH + TEMPLATES['benefit_add_form'])

    

def add_announcement(request):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/forbidden')

    if (request.method == "POST"):
        title = request.POST['title']
        summary = request.POST['summary']
        description = request.POST['description']

        image = None
        if request.FILES.get('thumbnail') != None:
            image = request.FILES.get('thumbnail')

        mi.save_announcement(title, summary, description, image)

        if (request.POST.getlist('notify_subscribers') != []):
            SMS_MESSAGE = f"New Benefit!: {title}\n{summary}\n=====================\nDetails:\n{description}"
            thread = threading.Thread(target = messaging.send_batch_sms(SMS_MESSAGE, [messaging.format_local_number_philippines(i) for i in mi.get_phone_list_announcements()]), name = 'thread')
            thread.start()  
            # asyncio.create_task(messaging.send_batch_sms(f"{title}\n{summary}", [messaging.format_local_number_philippines(i) for i in mi.get_phone_list_benefits()]))

        return redirect('/announcements/')
    else:
        return render(request, MAIN_PATH + TEMPLATES['announcement_add_form'])

# need view for editing account details thansk