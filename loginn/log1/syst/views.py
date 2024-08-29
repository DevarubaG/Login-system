from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import re

# Create your views here.
def home(request):
    return render(request,"syst/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try another username")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered! Please try another email")
            return redirect('signup')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric")
            return redirect('signup')

        # Password validation
        password_errors = []

        if len(pass1) < 8:
            password_errors.append("Password must be at least 8 characters long")

        if not re.search(r'[A-Z]', pass1):
            password_errors.append("Password must contain at least one uppercase letter")

        if not re.search(r'[a-z]', pass1):
            password_errors.append("Password must contain at least one lowercase letter")

        if not re.search(r'[\W_]', pass1):
            password_errors.append("Password must contain at least one symbol")

        if password_errors:
            for error in password_errors:
                messages.error(request, error)
            return redirect('signup')

        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, "Your account has been successfully created.")
        return redirect('signin')

    return render(request, "syst/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "syst/index.html", {'fname': fname})
        else:
            messages.error(request, "Bad Credentials")
            return redirect('signin')

    return render(request, "syst/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")
