# Generated by Django 3.1.7 on 2021-04-09 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20210407_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='test', max_length=200, unique=True),
            preserve_default=False,
        ),
    ]