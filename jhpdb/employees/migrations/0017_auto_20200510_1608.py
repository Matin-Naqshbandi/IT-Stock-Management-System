# Generated by Django 3.0.5 on 2020-05-10 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0016_auto_20200510_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='extensionnumber',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='employees.Department'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalextensionnumber',
            name='department',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='employees.Department'),
        ),
    ]
