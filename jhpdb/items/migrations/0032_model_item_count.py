# Generated by Django 3.0.5 on 2020-05-05 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0031_remove_model_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='item_count',
            field=models.IntegerField(default=1),
        ),
    ]
