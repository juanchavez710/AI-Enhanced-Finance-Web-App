from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout
from .models import Stock, Profile
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return render(request, "home.html")
def disclaimers(request):
    return render(request, "disclaimers.html")
def logout_view(request):
    logout(request)
    return redirect("/")
# def profile(request):
#     return render(request, "profile.html")

#render stocks
def all_stocks(request):
    stock_list = Stock.objects.all()
    return render(request, "predictions.html", {'stock_list':stock_list})

def associate_stock(request, stock_id):
    stock = Stock.objects.get(pk=stock_id)
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if stock in user_profile.user_stocks.all():
            # If the stock is already associated, remove it
            user_profile.user_stocks.remove(stock)
        else:
            # If the stock is not associated, add it
            user_profile.user_stocks.add(stock)

    return redirect('stock_detail', stock_id=stock_id)

def stock_detail(request, stock_id):
    stock = Stock.objects.get(pk=stock_id)  # Retrieve the stock
    return render(request, 'stock_detail.html', {'stock': stock})

def profile(request):
    user = request.user  # Get the current user
    profile = user.profile  # Get the user's profile
    associated_stocks = profile.user_stocks.all()  # Retrieve the associated stocks

    return render(request, 'profile.html', {'associated_stocks': associated_stocks})

from django.shortcuts import render
from pymongo import MongoClient

# views.py
import matplotlib.pyplot as plt
import pandas as pd
from django.http import HttpResponse
from pymongo import MongoClient
from io import BytesIO

def stock_graph(request, symbol):
    client = MongoClient("mongodb+srv://juanchavez:64TtcwjP5rMfV@cluster0.gtl8kn3.mongodb.net/?retryWrites=true&w=majority")
    db = client['AIEFAStocks']
    collection = db[symbol]
    data = collection.find()

    # Prepare data
    dates = []
    closing_prices = []
    predicted_prices = []
    for record in data:
        dates.append(record['Date'])
        closing_prices.append(record.get('Close'))
        predicted_prices.append(record.get('Predicted Price'))

    # Convert dates for matplotlib
    dates = pd.to_datetime(dates)

    # Create a figure and save it to a bytes buffer
    plt.figure(figsize=(10, 5))
    plt.plot(dates, closing_prices, label='Closing Price')
    plt.plot(dates, predicted_prices, label='Predicted Price', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Prices Over Time')
    plt.legend()
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')

