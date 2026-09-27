import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

from .utils import GLOBAL_CONTEXT

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        
        return redirect("main:login")

    context = {
        "form": form,
    }

    return render(request, "register.html", GLOBAL_CONTEXT(request) | context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        
        login(request, user)
        
        response = redirect("main:show_main")
        response.set_cookie("last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        return response

    context = {
        "form": form,
    }

    return render(request, "login.html", GLOBAL_CONTEXT(request) | context)

def logout_user(request):
    logout(request)
    
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    
    return response
