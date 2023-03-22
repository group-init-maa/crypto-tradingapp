from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from CryptoTrader import settings
from django.contrib.auth import authenticate, login, logout
import base64
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2 import service_account
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def index(request):
    return render(request, "login/index.html")

def home(request):
    return render(request, "/Users/maxwardle/Desktop/Bootcamp/Team Projects/crypto-tradingapp-2/CryptoTrader/login/templates/home.html")

def signin(request):
    signup_success = None
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Incorrect username or password.")
            return redirect("signin")
    else:
        if request.method == "GET" and messages.get_messages(request):
            messages_list = messages.get_messages(request)
            for message in messages_list:
                if message.tags == "success":
                    signup_success = message
            return render(request, "login/signin.html", {"signup_success": signup_success})
        else:
            return render(request, "login/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "logged out successfully!")
    return redirect("loginpage")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "username already exists, try another username")
            return redirect("signup")
        
        # if User.objects.filter(email=email).exists():
        #     messages.error(request, "email is already registered")
        #     return redirect("signup")
        
        if len(username) > 10:
            messages.error(request, "username must be under 10 characters")
            return redirect("signup")
    
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Your account has been created. Please sign in to continue.")
        except IntegrityError:
            messages.error(request, "Username already exists.")
            return redirect("signup")
        
        # send welcome email
        subject = "Welcome to the Crypto Trader"
        message = f"Hello {user.username}!!\nWelcome to our crypto trading simulator. We have sent you a confirmation email, please confirm your email address in order to activate your account." 
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect("signin")

    else:
        return render(request, "login/signup.html")
        
# Paste the code from the previous prompt here
def send_email(to, subject, body):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            'CryptoTrader/services/client_secret_1805964169-9a94vdqv054k28qe7t2v9u9r452f23bk.apps.googleusercontent.com.json',
            scopes=['https://www.googleapis.com/auth/gmail.compose']
        )

        service = build('gmail', 'v1', credentials=credentials)

        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject

        text = MIMEText(body)
        message.attach(text)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        send_message = (service.users().messages().send(userId="me", body={'raw': raw_message}).execute())

        print(F'sent message to {to} Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message