# Generated by Django 3.1.7 on 2021-03-24 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
    ]
