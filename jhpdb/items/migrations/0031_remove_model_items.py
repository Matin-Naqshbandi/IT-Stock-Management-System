# Generated by Django 3.0.5 on 2020-05-05 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0030_model_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='model',
            name='items',
        ),
    ]
