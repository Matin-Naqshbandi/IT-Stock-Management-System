# Generated by Django 3.0.5 on 2020-04-23 15:15

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_auto_20200416_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=smart_selects.db_fields.GroupedForeignKey(group_field='manufacturer', on_delete=django.db.models.deletion.CASCADE, to='items.Category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='model',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='category', chained_model_field='category', on_delete=django.db.models.deletion.CASCADE, to='items.Model'),
        ),
    ]
