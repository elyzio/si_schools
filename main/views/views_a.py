from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def Login(request):
    
    context = {
        'page_title': 'Login',
    }
    return render(request, 'auth/login.html', context)

# @login_required
def Logout(request):
    logout(request)
    context = {
        'page_title': 'Logout',
    }
    return render(request, 'auth/logout.html', context)