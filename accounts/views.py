from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.

def register_page(request):
    return render(request, "account/auth/register.html")

def login_page(request):
    
    # Check if user is already logged in
    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in.')
        return redirect('dashboard_home')
    
    return render(request, "account/auth/login.html")

def forgot_password_page(request):
    return render(request, "account/auth/forgot_password.html")

def reset_password_page(request):
    return render(request, "account/auth/reset_password.html")

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/account/login/')
