import os
import django
import csv


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AIEFAapp.settings")  # Replace with your project name
django.setup()

from AIEFAapp.models import Stock
from django.templatetags.static import static

relative_path = 'stockdata.csv'

static_url = static(relative_path)
print(static_url)

with open('stockdata.csv', 'r') as csvfile:  # Replace 'stock_data.csv' with your data source
    reader = csv.DictReader(csvfile)
    for row in reader:
        stock = Stock(
            symbol=row['symbol'],
            name=row['name'],
            graph=row['graph_data']
        )
        stock.save()