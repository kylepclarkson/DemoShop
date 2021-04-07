# Generated by Django 3.1.7 on 2021-04-06 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=250)),
                ('postal_code', models.CharField(max_length=12)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='braintree_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='postal_code',
        ),
        migrations.AddField(
            model_name='order',
            name='mailing_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.mailingaddress'),
        ),
    ]
