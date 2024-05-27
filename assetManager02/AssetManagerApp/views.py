from pyexpat.errors import messages
from django.db.models import manager
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from. forms import CreateSpaceForm, CreateUserForm, LoginForm, SpaceCodeForm
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group, Permission
from .models import Group
from .forms import GroupForm
from .models import spaceRoles
from django.db import models
from .forms import UserLogForm
from .models import UserLog
from .models import Space 
from django.utils import timezone

def sitehome(request):
 return render(request, "AssetManagerApp/index.html")


@login_required(login_url="login")
def homepage(request):
    space = Space.objects.all()
    
    
    if request.user.is_authenticated:
        user_spaces = Space.objects.filter(models.Q(owner=request.user) | models.Q(members=request.user)).distinct()
        form = SpaceCodeForm() 
        if request.method == 'POST':
            form = SpaceCodeForm(request.POST)
            if form.is_valid():
                code = form.cleaned_data['code']
                try:
                    space = Space.objects.get(code=code)
                    spaceRoles.objects.create(user=request.user, space=space, role='member')
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

def dashboard(request, space_id):
    space = get_object_or_404(Space, id=space_id)
    logs = UserLog.objects.filter(space=space).select_related('user')
    todo_logs = UserLog.objects.filter(space=space, user=request.user, return_by__isnull=False)
    space_members = space.members.all()
    
    if request.method == "POST":
        form = UserLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.space = space
            log.last_changed_by = form.cleaned_data['last_changed_by'] or request.user
            log.last_changed_date = form.cleaned_data['last_changed_date'] or timezone.now()
            log.save()
            
            messages.success(request, 'Log added successfully.')
            return redirect('dashboard', space_id=space_id)
        else:
            messages.error(request, 'Error adding log. Please check the form.')
    else:
        form = UserLogForm()
    
    user_logs = UserLog.objects.filter(space=space)
    return render(request, "AssetManagerApp/dashboard.html", {'form': form, 'user_logs': user_logs, 'space': space, 'todo_logs': todo_logs, 'space_members': space_members})
def logout(request):
    auth.logout(request)
    return redirect("login")
   
def newLog(request, space_id):
    space = get_object_or_404(Space, id=space_id)
    if request.method == "POST":
        form = UserLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.space = space
            log.last_changed_date = timezone.now()
            log.save()
            return redirect('dashboard', space_id=space_id)
    else:
        form = UserLogForm()
    user_logs = UserLog.objects.filter(space=space)
    return render(request, "AssetManagerApp/newLog.html", {'form': form, 'user_logs': user_logs, 'space': space})

def editLog(request, log_id, space_id):
    log = get_object_or_404(UserLog, id=log_id)
    space = get_object_or_404(Space, id=space_id)
    user_role = spaceRoles.objects.filter(user=request.user, space=space).first()

    if log.user != request.user and (user_role is None or user_role.role != 'owner'):
        messages.error(request, 'You do not have permission to edit this log.')
        return redirect('dashboard', space_id=space.id)

    if request.method == 'POST':
        form = UserLogForm(request.POST, instance=log)
        if form.is_valid():
            log = form.save(commit=False)
       
            if form.cleaned_data['last_changed_date']:
                log.last_changed_date = form.cleaned_data['last_changed_date']
            else:
                log.last_changed_date = timezone.now() 
            
          
            if form.cleaned_data['return_by']:
                log.return_by = form.cleaned_data['return_by']
                log.email = form.cleaned_data['email']
            log.save()
            messages.success(request, 'Log updated successfully.')
            return redirect('dashboard', space_id=space.id)
        else:
            messages.error(request, 'Error updating log. Please check the form.')
    else:
        form = UserLogForm(instance=log)
    
    return render(request, "AssetManagerApp/editLog.html", {'form': form, 'space': space})
@login_required
def deleteLog(request, log_id, space_id):
    log = get_object_or_404(UserLog, id=log_id)
    space = get_object_or_404(Space, id=space_id)

    user_role = spaceRoles.objects.filter(user=request.user, space=space).first()

    if log.user != request.user and (user_role is None or user_role.role != 'owner'):
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        log.delete()
        return redirect('dashboard', space_id=space_id)
    return render(request, 'AssetManagerApp/deleteLog.html', {'log': log})
    

def spaceCreate(request):
    if request.method == 'POST':
        form = CreateSpaceForm(request.POST)
        if form.is_valid():
            space = form.save(commit=False)
            space.owner = request.user
            space.save()
            spaceRoles.objects.create(user=request.user, space=space, role='owner')
            return redirect('homepage')
        
    else:
        form = CreateSpaceForm()
    return render(request, "AssetManagerApp/SpaceCreate.html")

def spaceManage(request, space_id):
    space = get_object_or_404(Space, id=space_id)
    members = space.members.all()
    return render(request, "AssetManagerApp/spaceManage.html", {'space': space, 'members': members})

def deleteSpace(request, space_id):
    space = get_object_or_404(Space, id=space_id)

    if space.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this space.")
    
    space.delete()
    return redirect('homepage')

def calendar(request):
    return render(request, "AssetManagerApp/calendar.html")
    

