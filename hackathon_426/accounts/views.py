from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login 
from .forms import LoginForm, PasswordResetForm

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

def password_reset_view(request):
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        verification_code = form.cleaned_data.get("verification_code")
        return redirect("password_reset_done")

    return render(request, "accounts/password_reset.html", {"form": form})

def home_view(request):
    return render(request, "accounts/home.html")