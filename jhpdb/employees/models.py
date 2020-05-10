from django.db import models
from django.utils import timezone
import datetime
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from smart_selects.db_fields import ChainedForeignKey
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from django.utils.timesince import timeuntil
from django.core.validators import RegexValidator

# Create your models here.

class Department(models.Model):
    department = models.CharField(max_length=255, unique=True)    
    history = HistoricalRecords()
    def __str__(self):
        return self.department

class Position(models.Model):
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    position = models.CharField(max_length=255)
    history = HistoricalRecords()
    class Meta:
        unique_together = ('department', 'position')
    def __str__(self):
        return self.position
    
class Province(models.Model):
    Badakhshan =  'Badakhshan'
    Badghis =  'Badghis'
    Baghlan =  'Baghlan'
    Balkh =  'Balkh'
    Bamyan =  'Bamyan'
    Daykundi =  'Daykundi'
    Farah =  'Farah'
    Faryab =  'Faryab'
    Ghazni =  'Ghazni'
    Ghor =  'Ghor'
    Helmand =  'Helmand'
    Herat =  'Herat'
    Jowzjan =  'Jowzjan'
    Kabul =  'Kabul'
    Kandahar =  'Kandahar'
    Kapisa =  'Kapisa'
    Khost =  'Khost'
    Kunar =  'Kunar'
    Kunduz =  'Kunduz'
    Laghman =  'Laghman'
    Logar =  'Logar'
    Nangarhar =  'Nangarhar'
    Nimruz =  'Nimruz'
    Nuristan =  'Nuristan'
    Paktia =  'Paktia'
    Paktika =  'Paktika'
    Panjshir =  'Panjshir'
    Parwan =  'Parwan'
    Samangan =  'Samangan'
    SarePol =  'Sar-e Pol'
    Takhar =  'Takhar'
    Urozgan =  'Urozgan'
    Wardak =  'Wardak'
    Zabul =  'Zabul'

    province_choice = [ (Badakhshan, 'Badakhshan'),
                        (Badghis, 'Badghis'),
                        (Baghlan, 'Baghlan'),
                        (Balkh, 'Balkh'),
                        (Bamyan, 'Bamyan'),
                        (Daykundi, 'Daykundi'),
                        (Farah, 'Farah'),
                        (Faryab, 'Faryab'),
                        (Ghazni, 'Ghazni'),
                        (Ghor, 'Ghor'),
                        (Helmand, 'Helmand'),
                        (Herat, 'Herat'),
                        (Jowzjan, 'Jowzjan'),
                        (Kabul, 'Kabul'),
                        (Kandahar, 'Kandahar'),
                        (Kapisa, 'Kapisa'),
                        (Khost, 'Khost'),
                        (Kunar, 'Kunar'),
                        (Kunduz, 'Kunduz'),
                        (Laghman, 'Laghman'),
                        (Logar, 'Logar'),
                        (Nangarhar, 'Nangarhar'),
                        (Nimruz, 'Nimruz'),
                        (Nuristan, 'Nuristan'),
                        (Paktia, 'Paktia'),
                        (Paktika, 'Paktika'),
                        (Panjshir, 'Panjshir'),
                        (Parwan, 'Parwan'),
                        (Samangan, 'Samangan'),
                        (SarePol, 'Sar-e Pol'),
                        (Takhar, 'Takhar'),
                        (Urozgan, 'Urozgan'),
                        (Wardak, 'Wardak'),
                        (Zabul, 'Zabul'),
                        ]
    province = models.CharField(max_length=10, choices=province_choice, unique=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.province

class Site(models.Model):
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    site = models.CharField(max_length=255)
    history = HistoricalRecords()
    class Meta:
        unique_together = ('province', 'site')
    def __str__(self):
        return self.site

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    province = models.ForeignKey(Province, on_delete=models.PROTECT, default=8)#default=Kabul
    site = ChainedForeignKey(Site,
                            chained_field="province",
                            chained_model_field="province",
                            show_all=False,
                            auto_choose=True,
                            sort=True, default=6#default=Main Office
                            )
    hire_date = models.DateField('Date Hired', default = timezone.now, null=True, blank=True)
    contract = models.IntegerField('Contract Months', default = 1, validators=[MaxValueValidator(100), MinValueValidator(1)])
    department = models.ForeignKey(Department, on_delete = models.PROTECT, default=9)#default=NotSpecified
    position = ChainedForeignKey(Position, 
                                chained_field="department", 
                                chained_model_field="department", 
                                show_all=False, 
                                auto_choose=True, 
                                sort=True, default=10#default=NotSpecified
                                )
    phonenumber = models.CharField(max_length=10, null=True, blank=True, unique=True, validators=[RegexValidator
                                                                            (regex='[0][7][02346789][0-9]{7}',
                                                                            message='Invalid Afghanistan Phone number',
                                                                            code='invalid_phone_number'),])
    skype = models.CharField(max_length=31, null=True, blank=True, unique=True, validators=[RegexValidator
                                                                            (regex='[a-zA-Z][a-zA-Z0-9\.,\-_]{5,31}',
                                                                            message='Invalid Skype ID',
                                                                            code='invalid_skype_id'),])
    history = HistoricalRecords()

    def timeuntil_out_of_contract(self):
        if date.today() >= self.hire_date + datetime.timedelta(days=self.contract*30):
            return ('Out of contract')
        else:
            return (timeuntil(self.hire_date + datetime.timedelta(days=self.contract*29)) , 'left')
    timeuntil_out_of_contract.admin_order_field = 'hire_date'
    timeuntil_out_of_contract.short_description = 'Contract info'

    def is_hired_recently(self):
        return self.hire_date >= date.today() - datetime.timedelta(days = 7)
    is_hired_recently.admin_order_field = 'hire_date'
    is_hired_recently.boolean = True
    is_hired_recently.short_description = 'Hired recently?'

    def __str__(self):
        return self.user.username

class ExtensionNumber(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    office = models.CharField(max_length=255)
    extension_number = models.CharField(max_length=3, unique=True, validators=[RegexValidator
                                                                            (regex='[6][0-4][0-9]',
                                                                            message='Invalid Extension number',
                                                                            code='invalid_extension_number'),])
    history = HistoricalRecords()
    def __str__(self):
        return self.extension_number
    