# Generated by Django 3.0.5 on 2020-04-29 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0016_auto_20200429_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='in_stock',
            field=models.BooleanField(default=True),
        ),
    ]