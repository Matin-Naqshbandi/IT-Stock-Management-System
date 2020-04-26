from django.db import models
from smart_selects.db_fields import ChainedManyToManyField, ChainedForeignKey

# Create your models here.

class Manufacturer(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    def __str__(self):
        return self.name

class Category(models.Model):
    category = models.CharField(max_length=255, null=False, blank=False)
    manufacturers = models.ManyToManyField('Manufacturer')
    def __str__(self):
        return self.category

class Model(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    category = ChainedForeignKey(
        Category,
        chained_field = 'manufacturer',
        chained_model_field = 'manufacturers',
    )
    model = models.CharField(max_length=255, null=False, blank=False)
    def __str__(self):
        return self.model

class Item(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    category = ChainedForeignKey(
        Category, 
        chained_field="manufacturer", 
        chained_model_field="manufacturers", 
        auto_choose=True, 
        show_all=False,
        sort=True
    )
    model = ChainedForeignKey(
        Model, 
        chained_field="category", 
        chained_model_field="category", 
        auto_choose=True, 
        show_all=False,
        sort=True
    )
    serial = models.CharField(max_length=255, unique=True, null=True, blank=True)
    tag_no = models.IntegerField(null=True, blank=True, unique=True)
    note = models.TextField(max_length=1024, null=True, blank=True)
    def __str__(self):
        return self.serial

class SpecList(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class SpecInfo(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    spec = models.ForeignKey(SpecList, on_delete=models.PROTECT)
    info = models.CharField(max_length=255, db_index=True)
    def __str__(self):
        return self.info

