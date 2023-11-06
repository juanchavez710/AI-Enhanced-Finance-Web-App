# Generated by Django 4.2.5 on 2023-10-20 16:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AIEFAapp', '0003_remove_stock_graph_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
