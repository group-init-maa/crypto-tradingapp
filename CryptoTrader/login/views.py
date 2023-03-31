import json
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Coin, UserProfile, Portfolio, Transaction
from django.contrib import messages
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist

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
            return redirect("signin")
        except IntegrityError:
            messages.error(request, "Username already exists.")
            return redirect("signup")
    else:
        return render(request, "login/signup.html")

        



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

        # Calculate the total cost of the transaction
        cost = Decimal(str(amount)) * Decimal(str(price))
        
        # Check if the user has enough balance
        if user.userprofile.balance < cost:
            # Return an error message if the user doesn't have enough balance
            messages.error(request, 'You do not have enough balance to complete this transaction.')
            return redirect('home')
        else:
            # Check if there is already a transaction for this coin and portfolio
            try:
                transaction = portfolio.transaction_set.filter(coin=coin_obj).first()
                if transaction is None:
                    # Create a new transaction object and save it
                    transaction = Transaction(portfolio=portfolio, coin=coin_obj, transaction_type='BUY', quantity=amount, price=price, balance=user.userprofile.balance)
                else:
                    # If the transaction exists, update the quantity
                    transaction.quantity += Decimal(str(amount))
                transaction.save()
            except ObjectDoesNotExist:
                # Create a new transaction object and save it
                transaction = Transaction(portfolio=portfolio, coin=coin_obj, transaction_type='BUY', quantity=amount, price=price, balance=user.userprofile.balance)
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
        print(total_quantity)
        if total_quantity < Decimal(str(amount)):
            # Return an error message if the user doesn't have enough of this coin to sell
            messages.error(request, f'You do not have {amount} {coin_obj.symbol} to sell.')
            return redirect('home')

        # Calculate the total proceeds from the sale
        sale_proceeds = Decimal(str(amount)) * coin_obj.price

        # Update the relevant transaction with the new quantity
        quantity_to_sell = Decimal(amount)
        for transaction in transactions:
            if quantity_to_sell == 0:
                break
            if transaction.quantity <= quantity_to_sell:
                # The entire transaction can be sold
                quantity_to_sell -= transaction.quantity
                transaction.delete()
            else:
                # Only a portion of the transaction can be sold
                transaction.quantity -= quantity_to_sell
                transaction.save()
                quantity_to_sell = 0


        # Create a new transaction object for the sale and save it
        transaction = Transaction(portfolio=portfolio, coin=coin_obj, transaction_type='SELL', quantity=amount, price=coin_obj.price)
        transaction.save()

        # Redirect back to the home page
        messages.success(request, f'Successfully sold {amount} {coin_obj.symbol} for £{sale_proceeds}.')
        return redirect('home')


@login_required
def account(request):
    if request.method == "POST":
        user = request.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        try:
            Portfolio.objects.create(user_profile=user_profile)
            message = "Portfolio created successfully."
        except IntegrityError:
            message = "Portfolio already exists for this user."
        return render(request, 'login/account.html', {'message': message})
    else:
        return render(request, "login/account.html")



