from django.db import models
from smart_selects.db_fields import ChainedManyToManyField, ChainedForeignKey
from employees.models import Employee
from django.utils import timezone
import datetime
from datetime import date
from .validators import validate_future
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
    expendable = models.BooleanField(default=False)
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
    status = models.CharField(max_length=255, default='In stock')
    def __str__(self):
        return (self.manufacturer.name+" "+self.model.model)

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

class ItemAssign(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    assign_to = models.ForeignKey(Employee, related_name='assigned_to', on_delete=models.DO_NOTHING)
    assigned_date = models.DateTimeField(default = timezone.now, validators=[validate_future], unique=True)
    assign_by = models.ForeignKey(Employee, related_name='assigned_by', on_delete=models.DO_NOTHING)
    received_date = models.DateTimeField(null=True, blank=True, validators=[validate_future], unique=True)
    received_by = models.ForeignKey(Employee, related_name='received_by', null=True, blank=True, on_delete=models.DO_NOTHING)
    Assigned = '0'
    Received = '1'
    Expended = '2'
    Lost = '3'
    Damaged = '4'
    assign_status_choice = [(Assigned, 'Assigned'), (Received, 'Received'), (Expended, 'Expended'), (Lost, 'Lost'), (Damaged, 'Damaged')]
    assign_status = models.CharField(max_length=1, choices=assign_status_choice, default=Assigned)

    def save(self):
        if ((self.item.status=='In stock') and (not self.pk) and (self.assign_status=='0') and (self.assign_to.user.is_active)):
            super(ItemAssign, self).save()
        elif ((self.item.status=='In stock') and (not self.pk) and (self.assign_status=='0') and (not self.assign_to.user.is_active)):
            raise Exception('Cannot be assign to inactive employees!')
        elif((self.item.status=='In stock') and (not self.pk) and (self.assign_status!='0')):
            raise Exception('Cannot be (Receive/Expended/Lost/Damaged) before assigning!')
        elif((self.item.status!='In stock') and (not self.pk) and (self.assign_status=='0')):
            raise Exception('Cannot Assign (Assigned/Expended/Lost/Damaged) item!')
        elif((self.item.status!='Assigned to '+self.assign_to.user.username) and (self.pk)):
            raise Exception('Cannot change (Item/Assign to/Assign status)')
        elif((self.item.status=='Assigned to '+self.assign_to.user.username) and (self.pk) and (self.assign_status=='2') and (not self.item.model.expendable)):
            raise Exception('Cannot Expend Unexpendable item')
        elif((self.item.status=='Assigned to '+self.assign_to.user.username) and (self.pk) and (self.assign_status!='0')):
            super(ItemAssign, self).save()
        else:
            raise Exception('Invalid Entry! (from items.models.ItemAssign.save)')

    def __str__(self):
        return (self.item.manufacturer.name+" "+self.item.model.model)

