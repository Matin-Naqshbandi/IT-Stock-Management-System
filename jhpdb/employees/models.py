from django.db import models
from django.utils import timezone
import datetime
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from smart_selects.db_fields import ChainedForeignKey
from simple_history.models import HistoricalRecords


# Create your models here.

class Department(models.Model):
    department = models.CharField(max_length=255, unique=True)    
    history = HistoricalRecords()
    def __str__(self):
        return self.department

class Position(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
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
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    site = models.CharField(max_length=255)
    history = HistoricalRecords()
    class Meta:
        unique_together = ('province', 'site')

    def __str__(self):
        return self.site

class Employee(models.Model):

    province = models.ForeignKey(Province, null=False, blank=False, on_delete=models.CASCADE)
    site = ChainedForeignKey('Site',
                            chained_field="province",
                            chained_model_field="province",
                            show_all=False,
                            auto_choose=True,
                            sort=True
                            )
    hire_date = models.DateField('Date Hired', default = timezone.now)
    contract = models.IntegerField('Contract Months',default = 1, validators=[MaxValueValidator(100), MinValueValidator(1)])
    department = models.ForeignKey(Department, null=False, blank=False, on_delete = models.CASCADE)
    position = ChainedForeignKey('Position', 
                                chained_field="department", 
                                chained_model_field="department", 
                                show_all=False, 
                                auto_choose=True, 
                                sort=True
                                )
    history = HistoricalRecords()

    def still_hired(self):
        return date.today() <= self.hire_date + datetime.timedelta(days=self.contract*30)
    still_hired.admin_order_field = 'entry_date'
    still_hired.boolean = True
    still_hired.short_description = 'Still hired?'

    def is_hired_recently(self):
        return self.hire_date >= date.today() - datetime.timedelta(days = 7)
    is_hired_recently.admin_order_field = 'entry_date'
    is_hired_recently.boolean = True
    is_hired_recently.short_description = 'Hired recently?'


    # def __str__(self):
    #     return self.hire_date