# Generated by Django 3.0.5 on 2020-04-30 13:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0007_auto_20200429_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='employees.Department'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='hire_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date Hired'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='department', chained_model_field='department', null=True, on_delete=django.db.models.deletion.CASCADE, to='employees.Position'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='employees.Province'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='site',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='province', chained_model_field='province', null=True, on_delete=django.db.models.deletion.CASCADE, to='employees.Site'),
        ),
        migrations.AlterField(
            model_name='historicalemployee',
            name='hire_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date Hired'),
        ),
    ]
