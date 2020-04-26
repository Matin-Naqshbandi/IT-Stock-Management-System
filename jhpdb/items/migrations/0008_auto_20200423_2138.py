# Generated by Django 3.0.5 on 2020-04-23 17:08

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0007_auto_20200423_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='manufacturer', chained_model_field='manufacturers', on_delete=django.db.models.deletion.CASCADE, to='items.Category'),
        ),
    ]
