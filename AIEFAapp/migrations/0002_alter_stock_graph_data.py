# Generated by Django 4.2.5 on 2023-10-19 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIEFAapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='graph_data',
            field=models.JSONField(),
        ),
    ]
