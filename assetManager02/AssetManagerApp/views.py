from pyexpat.errors import messages
from django.db.models import manager
from django.shortcuts import get_object_or_404, render, redirect
import AssetManagerApp

from. forms import CreateSpaceForm, CreateUserForm, LoginForm, SpaceCodeForm

from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group, Permission

from django.db import models
from .forms import UserLogForm
from .models import UserLog
from .models import Space 

def sitehome(request):
 return render(request, "AssetManagerApp/index.html")

@login_required(login_url="login")
def homepage(request):
    spaces = Space.objects.all()
    
    if request.user.is_authenticated:
        user_spaces = Space.objects.filter(models.Q(owner=request.user) | models.Q(members=request.user)).distinct()
        form = SpaceCodeForm() 
        if request.method == 'POST':
            form = SpaceCodeForm(request.POST)
            if form.is_valid():
                code = form.cleaned_data['code']
                try:
                    space = Space.objects.get(code=code)
                    
                    space.members.add(request.user)
                    return redirect('homepage')  
                except Space.DoesNotExist:
                    messages.error(request, 'Invalid space code. Please try again.')
        return render(request, "AssetManagerApp/homepage.html", {'user_spaces': user_spaces, 'form': form})
    
    else:
        return render(request, "AssetManagerApp/homepage.html")


def register(request):
    
    form = CreateUserForm
    
    if request.method == "POST":
        
        form = CreateUserForm(request.POST) 

        if form.is_valid():
         
            form.save()
         
            return redirect("login")
     
    context = {'registerform':form}

    return render(request, "AssetManagerApp/register.html", context=context)


def login(request):
    
    form = LoginForm()
    
    if request.method == 'POST':
        
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
         
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                
                auth.login(request, user)
                
                return redirect("homepage")
            
    context = {'loginform':form}
    
    return render(request, "AssetManagerApp/login.html",context=context)

@login_required(login_url="login")
def dashboard(request, space_id):
    
    space = get_object_or_404(Space, id=space_id)
    
    if request.method == "POST":
       form = UserLogForm(request.POST)
       if form.is_valid():
           log = form.save(commit=False)
           log.user = request.user
           log.space = space
           log.save()
           
           return redirect('dashboard', space_id=space_id)   
        
    else:
        form = UserLogForm()
    
    user_logs = UserLog.objects.filter(space=space)
    return render(request,"AssetManagerApp/dashboard.html", {'form': form, 'user_logs': user_logs, 'space': space})


def logout(request):
    
    auth.logout(request)
    
    return redirect("")
    
def newLog(request, space_id):
    space = get_object_or_404(Space, id=space_id)
    form = UserLogForm()
    if request.method == "POST":
        form = UserLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.space = space
            log.save()
            return redirect('dashboard', space_id=space_id)
    user_logs = UserLog.objects.filter(user=request.user)
    return render(request, "AssetManagerApp/newLog.html", {'form': form, 'user_logs': user_logs})
   
def editLog(request, log_id, space_id):
    log = get_object_or_404(UserLog, id=log_id)
    space = get_object_or_404(Space, id=space_id)

    if request.method == 'POST':
        form = UserLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            return redirect('dashboard', space_id=space_id)
    else:
        form = UserLogForm(instance=log)
    return render(request, "AssetManagerApp/editLog.html", {'form': form})    

@login_required
@permission_required('AssetManagerApp.delete_log', raise_exception=True)
def deleteLog(request, log_id, space_id):
    log = get_object_or_404(UserLog, id=log_id)
    space = get_object_or_404(Space, id=space_id)
    log.delete()
    return redirect('dashboard', space_id=space_id)
    

def spaceCreate(request):
    if request.method == 'POST':
        form = CreateSpaceForm(request.POST)
        if form.is_valid():
            new_space = form.save(commit=False)
            new_space.owner = request.user
            new_space.save()
            return redirect('homepage')
        
    else:
        form = CreateSpaceForm()
    return render(request, "AssetManagerApp/spaceCreate.html")

def spaceManage(request, space_id):
    space = get_object_or_404(Space, id=space_id)
    members = space.members.all()
    return render(request, "AssetManagerApp/spaceManage.html", {'space': space, 'members': members})
    