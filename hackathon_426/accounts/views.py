from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login 
from .forms import LoginForm

# Create your views here.
def login_view(request): 
    form = LoginForm(request.POST or None)
    if form.is_valid(): 
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            form.add_error(None, "Invalid credentials")

    return render(request, "accounts/login.html", {"form": form})

def home_view(request):
    return render(request, "accounts/home.html")