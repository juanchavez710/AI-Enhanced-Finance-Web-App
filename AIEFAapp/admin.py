from django.contrib import admin
from .models import Stock, Profile, StockData

# Register your models here.

admin.site.register(Stock)
admin.site.register(Profile)
admin.site.register(StockData)