import json
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import requests
from .models import Coin, UserProfile, Portfolio, Transaction
from django.contrib import messages
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from CryptoTrader import settings
from django.contrib.auth import authenticate, login, logout
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decimal import Decimal


def index(request):
    return render(request, "login/signin.html")

import json
from decimal import Decimal


@login_required
def home(request):
    try:
        user_profile = request.user.userprofile
        balance_history = user_profile.balance_history()
        balance_history = [(str(date), float(value)) for date, value in balance_history]
        context = {
        'user': request.user,
        'balance_history_json': json.dumps(balance_history),
        }
        return render(request, 'login/home.html', context)
    except ObjectDoesNotExist:
        return render(request, 'login/home.html')


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
    return redirect("signin")


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
        

from django.core.exceptions import ObjectDoesNotExist

def buy(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        coin = request.POST.get('coin')
        
        # Get the current user and their portfolio
        user = request.user
        portfolio = user.userprofile.portfolio
        
        try:
            # Get the price of the coin
            coin_obj = Coin.objects.get(name=coin)
        except ObjectDoesNotExist:
            messages.error(request, 'The coin you are trying to buy does not exist.')
            return redirect('home')
        
        price = coin_obj.price
        print(price)
        print(amount)

        # Calculate the total cost of the transaction
        cost = Decimal(str(amount)) * Decimal(str(price))
        print(cost)
        
        # Check if the user has enough balance
        if user.userprofile.balance < cost:
            # Return an error message if the user doesn't have enough balance
            messages.error(request, 'You do not have enough balance to complete this transaction.')
            return redirect('home')
        
        # Create a new transaction object and save it
        transaction = Transaction(portfolio=portfolio, coin=coin_obj, transaction_type='BUY', quantity=amount, price=price)
        transaction.save()

        # Deduct the cost of the transaction from the user's balance and save the changes
        user.userprofile.balance -= Decimal(str(cost))
        transaction.balance = user.userprofile.balance
        user.userprofile.save()
        transaction.save()

        # Redirect back to the home page
        messages.success(request, 'Transaction complete.')
        return redirect('home')


def sell(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        coin = request.POST.get('coin')

        # Get the current user and their portfolio
        user = request.user
        portfolio = user.userprofile.portfolio

        try:
            # Get the coin object from the database
            coin_obj = Coin.objects.get(name=coin)
        except ObjectDoesNotExist:
            messages.error(request, 'The coin you are trying to sell does not exist.')
            return redirect('home')

        # Get the user's transaction history for this coin
        transactions = Transaction.objects.filter(portfolio=portfolio, coin=coin_obj).order_by('timestamp')

        # Check if the user has enough of this coin to sell
        total_quantity = sum([transaction.quantity for transaction in transactions])
        if total_quantity < Decimal(str(amount)):
            # Return an error message if the user doesn't have enough of this coin to sell
            messages.error(request, f'You do not have {amount} {coin_obj.symbol} to sell.')
            return redirect('home')

        # Calculate the total proceeds from the sale
        sale_proceeds = Decimal(str(amount)) * coin_obj.price

        # Create a new transaction object for the sale and save it
        transaction = Transaction(portfolio=portfolio, coin=coin_obj, transaction_type='SELL', quantity=amount, price=coin_obj.price)
        transaction.save()

        # Add the proceeds to the user's balance and save the changes
        user.userprofile.balance += sale_proceeds
        transaction.balance = user.userprofile.balance
        user.userprofile.save()
        transaction.save()

        # Redirect back to the home page
        messages.success(request, f'Successfully sold {amount} {coin_obj.symbol} for £{sale_proceeds}.')
        return redirect('home')

@login_required
def account(request):
    user_profile = request.user.userprofile
    coins = user_profile.portfolio.coins.all().values()
    return JsonResponse(list(coins), safe=False)



