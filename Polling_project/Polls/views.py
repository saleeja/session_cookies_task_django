from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Poll


def user_login(request):
    # If the request method is POST, attempt to authenticate the user
    if request.method == 'POST':
        # Retrieve username and password from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the user provided valid credentials
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # User provided valid credentials
            login(request, user)
            successful_logins = request.COOKIES.get('successful_logins', 0)
            successful_logins = int(successful_logins) + 1
            response = redirect('list_items')
            response.set_cookie('successful_logins', successful_logins)
            return response  
        else:
            # User provided invalid credentials
            request.session['failed_login_attempts'] = request.session.get('failed_login_attempts', 0) + 1
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
         # If the request method is not POST, render the login page
         return render(request, 'login.html')


@login_required
def user_logout(request):
    # Logout the user and redirect to the login page
    logout(request)
    return redirect('user_login')

@login_required
def list_items(request):
    # Retrieve all polls from the database and render the poll list page
    polls = Poll.objects.all()
    return render(request, 'poll_list.html', {'polls': polls})


def login_attempts(request):
    successful_logins = request.session.get('successful_logins', 0)
    failed_login_attempts = request.session.get('failed_login_attempts', 0)
    cookies = request.COOKIES
    session_id = request.session.session_key
    return render(request, 'login_attempts.html', {'successful_logins': successful_logins, 'failed_login_attempts': failed_login_attempts, 'cookies': cookies, 'session_id': session_id})


