# Generated by Django 3.0.5 on 2020-04-29 13:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0012_itemlifecycle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemlifecycle',
            name='assign_date_end',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='itemlifecycle',
            name='assign_date_start',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
