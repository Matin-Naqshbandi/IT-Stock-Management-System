# Generated by Django 3.0.5 on 2020-04-29 13:49

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0007_auto_20200429_1721'),
        ('items', '0011_auto_20200426_1600'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemLifeCycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assign_date_start', models.DateTimeField(default=datetime.datetime(2020, 4, 29, 13, 49, 1, 866769, tzinfo=utc))),
                ('assign_date_end', models.DateTimeField(blank=True, default=datetime.datetime(2020, 4, 29, 13, 49, 1, 866769, tzinfo=utc), null=True)),
                ('assign_confirm', models.BooleanField(blank=True, null=True)),
                ('assign_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_by', to='employees.Employee')),
                ('assign_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_to', to='employees.Employee')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.Item')),
            ],
        ),
    ]