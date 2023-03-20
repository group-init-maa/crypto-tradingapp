from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
# Create your views here.

def index(request):
    responseData = render_to_string("login\login.html")
    return HttpResponse(responseData)

def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
    
    myuser = User.objects.create_user(username, email, password)

    myuser.save()
    subject = "Welcome to GFG- Django Login!!"
    message = "Hello " + myuser.first_name + "!! \n" + "Welcome to GFG!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"        
    from_email = settings.EMAIL_HOST_USER
    to_list = [myuser.email]
    send_mail(subject, message, from_email, to_list, fail_silently=True)
    
    messages.success(request, "Your account has been made ! :3")


    return redirect("signin")

def signout(request):
    return render(request, "login/signout.html")

def singup(request):
    return render(request, "login/signup.html")