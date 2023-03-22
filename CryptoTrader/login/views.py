from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.db.utils import IntegrityError
from CryptoTrader import settings
from django.contrib.auth.models import User
from django.contrib import messages

# from geeksforgeeks import settings
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate, login, logout
# from . tokens import generate_token


# Create your views here.

def index(request):
    responseData = render_to_string("login\login.html")
    return HttpResponse(responseData)

def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            fname = user.username
            return render (request, "login/index.html", {'name': username})
        else:
            messages.error(request, "incorrect username or password")
            return redirect("home")
    return render(request, "login/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "logged out successfully!")
    return redirect("home")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        if User.objects.filter(username = username):
            messages.error(request, "username already exists, try another username")
            return redirect("home")
        
        if User.objects.filter(email = email):
            messages.error(request, "email is already registered")
            return redirect("home")
        
        if len(username) > 10:
            messages.error(request, "username must be under 10 characters")
    
        try:
            myuser = User.objects.create_user(username, email, password)
        except IntegrityError:
            messages.error(request, "Username already exists.")
            error_message = "Username already exists."
            return render(request, "login/error.html", {"error_message": error_message})

        messages.success(request, "Your account has been made!")

        # welcome email

        subject = "welcome to the crypto trader"
        message = "Hello " + myuser.username + "!! \n" + "welcome to our crypto trading simulator \n we have sent you a confirmation email, please confirm your email address in order to activate your account" 
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently = True)

        return redirect("signin")

    else:
        return render(request, "login/signup.html")
    
    