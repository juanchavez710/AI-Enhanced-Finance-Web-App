from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    hist_accuracy = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return f"{self.symbol}"
    
class StockData(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    closing_price = models.DecimalField(max_digits=10, decimal_places=2)
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.stock.symbol} on {self.date} - Closing: {self.closing_price}, Predicted: {self.predicted_price}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_stocks = models.ManyToManyField(Stock)
    
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.Profile.save()
    