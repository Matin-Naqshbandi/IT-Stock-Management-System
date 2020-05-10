from django.db import models
from smart_selects.db_fields import ChainedManyToManyField, ChainedForeignKey
from employees.models import Employee
from django.utils import timezone
import datetime
from datetime import date
from .validators import validate_future
from django.core.validators import MaxValueValidator, MinValueValidator
from simple_history.models import HistoricalRecords
# Create your models here.

class Manufacturer(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    manufacturers = models.ManyToManyField('Manufacturer')
    history = HistoricalRecords()
    def __str__(self):
        return self.name

class Model(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT)
    category = ChainedForeignKey(
        Category,
        chained_field = 'manufacturer',
        chained_model_field = 'manufacturers',
        auto_choose=True, 
        show_all=False,
        sort=True
    )
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    expendable = models.BooleanField(default=False)
    item_count = models.IntegerField(default=1)
    history = HistoricalRecords()

    def item_in_stock(self):
        return Item.objects.filter(model=self.pk, status='In stock').count()
    item_in_stock.short_description = 'In Stock'
    def item_assigned(self):
        return Item.objects.filter(model=self.pk, status__contains='Assign to ').count()
    item_assigned.short_description = 'Assigned'
    def item_expended(self):
        return Item.objects.filter(model=self.pk, status__contains='Expended by ').count()
    item_expended.short_description = 'Expended'
    def item_lost(self):
        return Item.objects.filter(model=self.pk, status__contains='Lost by ').count()
    item_lost.short_description = 'Lost'
    def item_damaged(self):
        return Item.objects.filter(model=self.pk, status__contains='Damaged by ').count()
    item_damaged.short_description = 'Damaged'
    def __str__(self):
        return self.name

class Item(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT)
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
    history = HistoricalRecords()
    def has_note(self):
        if(self.note):
            return True
        else:
            return False
    has_note.boolean = True
            
    def __str__(self):
        return (self.manufacturer.name+" "+self.model.name)

class SpecList(models.Model):
    name = models.CharField(max_length=255)
    history = HistoricalRecords()
    def __str__(self):
        return self.name

class SpecInfo(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    spec = models.ForeignKey(SpecList, on_delete=models.PROTECT)
    info = models.CharField(max_length=255, db_index=True)
    history = HistoricalRecords()
    def save(self):
        self.info = self.info.upper()
        super(SpecInfo, self).save()
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
    history = HistoricalRecords()
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
        return (self.item.manufacturer.name+" "+self.item.model.name)

class PersonalDevice(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    device = models.CharField(max_length=255, null=True, blank=True)
    mac = models.CharField(max_length=17, null=True, blank=True, unique=True)
    history = HistoricalRecords()
    def save(self):
        self.mac = self.mac.upper()
        super(PersonalDevice, self).save()
    def __str__(self):
        return (self.employee.user.username+"'s "+self.device)