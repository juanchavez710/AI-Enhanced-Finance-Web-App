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
    django_stocks = Stock.objects.all()
    client = MongoClient("mongodb+srv://juanchavez:64TtcwjP5rMfV@cluster0.gtl8kn3.mongodb.net/?retryWrites=true&w=majority")
    db = client['historical_accuracy']
    collection = db['historical_accuracy']

    # Create a dictionary to hold accuracy data from MongoDB
    accuracy_data = {}
    for record in collection.find():
        accuracy_data[record['Stock Symbol']] = round(record['R-Squared'] * 100, 2)

    # Prepare combined stock data
    stocks = []
    for stock in django_stocks:
        symbol = stock.symbol  # Assuming 'symbol' is the field in your Stock model
        accuracy = accuracy_data.get(symbol, None)  # Get accuracy if it exists
        stocks.append({
            'id': stock.id,  # Include the Django model's id
            'symbol': symbol,
            'accuracy': accuracy
        })

    return render(request, "predictions.html", {'stocks': stocks})

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
    # Retrieve the stock from the Django model
    stock = Stock.objects.get(pk=stock_id)
    
    # MongoDB client setup
    client = MongoClient("mongodb+srv://juanchavez:64TtcwjP5rMfV@cluster0.gtl8kn3.mongodb.net/?retryWrites=true&w=majority")

    # Fetch historical accuracy
    db_historical_accuracy = client['historical_accuracy']
    collection_accuracy = db_historical_accuracy['historical_accuracy']
    accuracy_record = collection_accuracy.find_one({'Stock Symbol': stock.symbol})
    historical_accuracy = accuracy_record['R-Squared'] if accuracy_record else None

    # Fetch final predicted price
    db_stock_prices = client['AIEFAStocks']
    collection_prices = db_stock_prices[stock.symbol]
    last_price_record = collection_prices.find().sort('Date', -1).limit(1).next()
    final_predicted_price = last_price_record.get('Predicted Price') if last_price_record else None

    return render(request, 'stock_detail.html', {
        'stock': stock,
        'historical_accuracy': historical_accuracy,
        'final_predicted_price': final_predicted_price
    })

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

    df = pd.DataFrame(list(data))
    df = df.sort_values('Date')

    dates = pd.to_datetime(df['Date'])
    closing_prices = df['Close']
    predicted_prices = df['Predicted Price']

    # Assuming the last values in your DataFrame are the latest
    last_closing_price = closing_prices.iloc[-1]
    last_predicted_price = predicted_prices.iloc[-1]
    last_date = dates.iloc[-1]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, closing_prices, label='Closing Price')
    plt.plot(dates, predicted_prices, label='Predicted Price', linestyle='--')

    # Annotate last closing price
    plt.annotate(f'Last Closing: {last_closing_price}', 
                 xy=(last_date, last_closing_price),
                 xytext=(last_date, last_closing_price),
                 arrowprops=dict(facecolor='blue', shrink=0.05))

    # Annotate last predicted price
    plt.annotate(f'Last Predicted: {last_predicted_price}', 
                 xy=(last_date, last_predicted_price),
                 xytext=(last_date, last_predicted_price),
                 arrowprops=dict(facecolor='green', shrink=0.05))

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'Stock Prices for {symbol} Over Time')
    plt.legend()
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    plt.close()  # Close the plot to free memory

    return HttpResponse(buffer.getvalue(), content_type='image/png')


