# Generated by Django 3.0.5 on 2020-05-03 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0012_auto_20200503_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='province',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.PROTECT, to='employees.Province'),
        ),
        migrations.AlterField(
            model_name='historicalemployee',
            name='province',
            field=models.ForeignKey(blank=True, db_constraint=False, default=8, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='employees.Province'),
        ),
    ]