# Generated by Django 3.0.5 on 2020-05-03 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0023_auto_20200503_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(default='In stock', max_length=255),
        ),
    ]
