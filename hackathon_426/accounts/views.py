from django.shortcuts import get_object_or_404, render, redirect
from .models import newSubmission
from .forms import LoginForm, AccountDetailsForm, ResetPasswordForm
from django.contrib.auth.decorators import login_required

def home_view(request):
    return render(request, "accounts/home.html")

def login_view(request): 
    create_mode = 'create' in request.POST
    form = LoginForm(request.POST or None, create_mode=create_mode)

    if request.method == "POST":
        if form.is_valid():
            if create_mode:
                submission = form.save()
                request.session['submission_id'] = submission.id
                return redirect('account_details')
            else:
                try:
                    submission = newSubmission.objects.get(
                        username=form.cleaned_data['username'])
                    password = form.cleaned_data['password']
                    if submission.password != password:
                        form.add_error(None, "Incorrect username or password.")
                    else:
                        request.session['submission_id'] = submission.id
                        return redirect('dashboard')
                except newSubmission.DoesNotExist:
                    form.add_error(None, "Invalid username or password.")
    return render(request, "accounts/login.html", {"form": form})

def reset_password_view(request):
    # TODO: Implement password reset logic
    form = ResetPasswordForm(request.POST or None)
    return render(request, "accounts/reset_password.html", {"form": form})

def account_details_view(request):
    if request.method == 'POST':
        form = AccountDetailsForm(request.POST)
        if form.is_valid():
            # Create a new submission instance
            submission = newSubmission(
                name=form.cleaned_data['name'],
                major=form.cleaned_data['major'],
                gender=form.cleaned_data['gender'],
                race=form.cleaned_data['race'],
                sports=form.cleaned_data['sports']
            )
            submission.save()
            return redirect('home')  # Redirect to home page after successful submission
    else:
        form = AccountDetailsForm()
    
    return render(request, 'accounts/account_details.html', {'form': form})

def logout_view(request):
    request.session.flush() 
    return redirect('login')  