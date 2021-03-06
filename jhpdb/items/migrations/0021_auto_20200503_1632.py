# Generated by Django 3.0.5 on 2020-05-03 12:02

from django.db import migrations, models
import django.utils.timezone
import items.models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0020_auto_20200503_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemassign',
            name='assigned_date',
            field=models.DateTimeField(default=django.utils.timezone.now, unique=True, validators=[items.models.validate_future]),
        ),
        migrations.AlterField(
            model_name='itemassign',
            name='received_date',
            field=models.DateTimeField(blank=True, null=True, unique=True, validators=[items.models.validate_future]),
        ),
    ]
