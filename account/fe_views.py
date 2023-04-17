from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate ,login, logout
from account.forms import UserRegisterForm, UserEditForm
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
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            # print(username,password)
            user = authenticate(request, username = username , password = password)     
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            messages.success(request, 'Account is created for ' , username)

            return redirect('LoginForm')  
    else:
        form = UserRegisterForm()

    context = {}   
    context.update({'form1':form}) 
    return render(request, 'account/registerPage.html',context)

from django.shortcuts import render
from django.db.models import Q  # New
@login_required
def dashboard(request):
    search_post = request.GET.get('search')
    if search_post:
        users = User.objects.filter(Q(email__icontains=search_post) | Q(name__icontains=search_post) | Q(user_type__icontains=search_post)).order_by('-created_at')
    else:
        users = User.objects.all().order_by('-created_at')
    context={'request':request,'users':users}
    return render(request,"account/UserDashboard.html",context)

from services.models import Appointment,Notification
@login_required
def userdetails(request,pk):
    userdetail=User.objects.get(id=pk) 
    registerform=UserEditForm(instance=userdetail)
    # try:
    appointments = Appointment.objects.filter(created_by=User.objects.get(id=pk))
    notifications = Notification.objects.filter(created_by=User.objects.get(id=pk))
    # except : 
    #     pass
    if request.method=='POST':
        registerform=UserEditForm(request.POST,request.FILES,instance=userdetail)
        if registerform.is_valid():
            registerform.save()
            return redirect('dashboard')
        else:
            messages.warning(request,f'Username or Password is incorrect !!! ')


    context={'userdetail':userdetail,'registerform':registerform,'files':request.FILES,'appointments':appointments,'notifications':notifications}
    return render(request,"account/userdetailsform.html",context)

@login_required
def logoutuser(request):
    logout(request)
    return redirect('home')