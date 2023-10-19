from django.db import models

# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    graph_data = models.TextField()  # You can store prediction data in JSON format or other suitable format

    def __str__(self):
        return self.symbol