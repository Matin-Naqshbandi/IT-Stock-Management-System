# Generated by Django 3.0.5 on 2020-05-10 08:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0013_auto_20200503_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='phonenumber',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Invalid Afghanistan Phone number', regex='[0][7][024789][0-9]{7}')]),
        ),
        migrations.AddField(
            model_name='employee',
            name='skype',
            field=models.CharField(blank=True, max_length=31, null=True, validators=[django.core.validators.RegexValidator(code='invalid_skype_id', message='Invalid Skype ID', regex='[a-zA-Z][a-zA-Z0-9\\.,\\-_]{5,31}')]),
        ),
        migrations.AddField(
            model_name='historicalemployee',
            name='phonenumber',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Invalid Afghanistan Phone number', regex='[0][7][024789][0-9]{7}')]),
        ),
        migrations.AddField(
            model_name='historicalemployee',
            name='skype',
            field=models.CharField(blank=True, max_length=31, null=True, validators=[django.core.validators.RegexValidator(code='invalid_skype_id', message='Invalid Skype ID', regex='[a-zA-Z][a-zA-Z0-9\\.,\\-_]{5,31}')]),
        ),
    ]
