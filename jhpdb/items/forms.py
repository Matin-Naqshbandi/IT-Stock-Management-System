from django import forms
from .models import *
from smart_selects.form_fields import ChainedModelChoiceField
from django.http import HttpResponse

# class ItemForm(forms.ModelForm):
#     class Meta: 
#         model = Item
#         fields = ['manufacturer', 'category', 'model', 'serial', 'tag_no']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['category'].queryset = Category.objects.none()
#         self.fields['model'].queryset = Model.objects.none()

#         if 'manufacturer' in self.data:
#             try:
#                 manufacturer_id = int(self.data.get('manufacturer'))
#                 self.fields['category'].queryset = Category.objects.filter(manufacturer_id=manufacturer_id).order_by('name')
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to empty Category queryset
#         elif self.instance.pk:
#             self.fields['category'].queryset = self.instance.manufacturer.category_set.order_by('name')