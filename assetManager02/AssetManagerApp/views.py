from django.db.models import manager
from django.shortcuts import get_object_or_404, render, redirect
from. forms import CreateSpaceForm, CreateUserForm, LoginForm

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .forms import UserLogForm
from .models import UserLog
from .models import Space, SpaceMemberManagment

def homepage(request):
    spaces = Space.objects.all()
    

    if request.user.is_authenticated:
        user_spaces = Space.objects.filter(owner=request.user)
        return render(request, "AssetManagerApp/index.html", {'user_spaces': user_spaces})
    
    else:
        return render(request, "AssetManagerApp/index.html")


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
                
                return redirect("dashboard")
            
    context = {'loginform':form}
    
    return render(request, "AssetManagerApp/login.html",context=context)

@login_required(login_url="login")
def dashboard(request):
    
    if request.method == "POST":
       form = UserLogForm(request.POST)
       if form.is_valid():
           log = form.save(commit=False)
           log.user = request.user
           log.save()
           
           return redirect('dashboard')   
        
    else:
        form = UserLogForm()
    
    user_logs = UserLog.objects.filter(user=request.user)
    return render(request,"AssetManagerApp/dashboard.html", {'form': form, 'user_logs': user_logs})


def logout(request):
    
    auth.logout(request)
    
    return redirect("")
    
def newLog(request):
    form = UserLogForm()
    if request.method == "POST":
        form = UserLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect('newLog')
    user_logs = UserLog.objects.filter(user=request.user)
    return render(request, "AssetManagerApp/newLog.html", {'form': form, 'user_logs': user_logs})
   
def editLog(request, log_id):
    log = get_object_or_404(UserLog, id=log_id)

    if request.method == 'POST':
        form = UserLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserLogForm(instance=log)
    return render(request, "AssetManagerApp/editLog.html", {'form': form})    

def deleteLog(request, log_id):
    log = get_object_or_404(UserLog, id=log_id)
    log.delete()
    return redirect('dashboard')
    
def spaceManage(request):  
    memberManagment = SpaceMemberManagment.objects.filter()
    return render(request, "AssetManagerApp/spaceManage.html", {'memberManagment': memberManagment })

def SpaceCreate(request):
    if request.method == 'POST':
        form = CreateSpaceForm(request.POST)
        if form.is_vaild():
            new_space = form.save(commit=False)
            new_space.owner = request.user
            new_space.save()
            return redirect('homepage')
        else:
            form = CreateSpaceForm()
            
            return render(request, "AssetManagerApp/SpaceCreate.html", {'form': form})
   
 
