# Generated by Django 4.2.5 on 2023-10-31 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIEFAapp', '0007_remove_profile_user_stocks_alter_stock_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='users',
            field=models.ManyToManyField(null=True, to='AIEFAapp.profile'),
        ),
    ]
