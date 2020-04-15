from django.db import models
from smart_selects.db_fields import ChainedManyToManyField, ChainedForeignKey

# Create your models here.

class Manufacturer(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)

class Category(models.Model):
    category = models.CharField(max_length=255, null=False, blank=False)
    manufacturers = models.ManyToManyField('Manufacturer')

class Model(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    category = ChainedManyToManyField(
        Category,
        horizontal=True,
        chained_field = 'manufacturer',
        chained_model_field = 'manufacturers',
    )
    model = models.CharField(max_length=255, null=False, blank=False)

class Item(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    category = ChainedForeignKey(
        Category, 
        chained_field="manufacturer", 
        chained_model_field="manufacturers", 
        auto_choose=True, 
        sort=True
    )
    model = ChainedForeignKey(
        Model, 
        chained_field="category", 
        chained_model_field="category", 
        auto_choose=True, 
        sort=True
    )
    serial = models.CharField(max_length=255)
    tag_no = models.IntegerField(null=False, blank=False)




# class MacAddress(models.Model):
#     LAN = '0'
#     WiFi = '1'
#     interface_choice = [(LAN = 'LAN'), (WiFi = 'WiFi')]
#     interface = models.CharField(max_length=1, choices=interface_choice, null=False, blank=False)
#     mac_address = models.CharField(max_length=12, null=False, blank=False, unique=True)
    