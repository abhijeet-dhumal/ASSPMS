from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate ,login, logout
from account.forms import UserRegisterForm, UserForm
from django.contrib import messages

from account.models import User
from services.models import Notification
from django.contrib.auth.decorators import login_required

def home(request):
    context={}
    return render(request,"account/home.html",context)

def LoginForm(request):
    try:
        if request.method =='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username , password = password)     
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return HttpResponse("<h1>Registered email or Password is incorrect !!!</h1>")
              
    except Exception as e:
        print(e)                

    context={}
    return render(request,"account/LoginForm.html",context)

def RegisterForm(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # form.save()
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            username = form.cleaned_data.get('username')
            
            messages.success(request, 'Account is created for ' , username)

            return redirect('LoginForm')  
    else:
        form = UserRegisterForm()

    context = {}   
    context.update({'form1':form}) 
    return render(request, 'account/registerPage.html',context)

@login_required
def dashboard(request):
    users=User.objects.all()
    context={'request':request,'users':users}
    return render(request,"account/UserDashboard.html",context)

@login_required
def userdetails(request,pk):
    userdetail=User.objects.get(id=pk)    
    registerform=UserForm(instance=userdetail)
    if request.method=='POST':
        registerform=UserForm(request.POST,request.FILES,instance=userdetail)
        if registerform.is_valid():
            registerform.save()
            return redirect('dashboard')
        else:
            messages.warning(request,f'Username or Password is incorrect !!! ')


    context={'userdetail':userdetail,'registerform':registerform,'files':request.FILES}
    return render(request,"account/userdetailsform.html",context)

@login_required
def logoutuser(request):
    logout(request)
    return redirect('home')