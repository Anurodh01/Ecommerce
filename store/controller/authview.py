from store.forms import CustomerUserForm
from django.contrib import messages
from django.shortcuts import redirect, render
from store.models import *
from django.contrib.auth import authenticate
from store.forms import CustomerUserForm 
from django.contrib.auth import login, logout
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form=CustomerUserForm()
    if request.method=="POST":
        form=CustomerUserForm(request.POST)
        if form.is_valid():
            form.save()
            print("hello")
            messages.success(request,"Registered Successfully!! Login to continue..")
            return redirect('/login')
    context={'form':form}
    return render(request,"store/auth/register.html",context)

def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already LoggedIN.")
        return redirect('home')
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        print(user)
        print(username,password)
        if user is not None:
            login(request,user)
            messages.success(request,"Logged in successfully")
            return redirect('home')
        else:
            messages.error(request,"Invalid username or password")
            return redirect('login')
    return render(request,'store/auth/login.html')

def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    return redirect('home')