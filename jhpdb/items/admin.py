from django.contrib import admin
from .models import *

# Register your models here.
class SpecInfoAdmin(admin.ModelAdmin):
    fieldsets = [('Specs Information: ', {'fields': ['item', 'spec', 'info']})]
    list_display = ['item', 'spec', 'info']
    list_filter = ['spec', 'item']
    search_fields = ['info',]

class SpecInfoInline(admin.TabularInline):
    model = SpecInfo
    extra = 1

class ItemAdmin(admin.ModelAdmin):
    fieldsets = [ ('Item Information: !!DO NOT ENTER USING ADMIN!!', {'fields': ['manufacturer', 'category', 'model','serial','tag_no', 'note']})]
    list_display = ['manufacturer', 'category', 'model','serial','tag_no']
    inlines = [SpecInfoInline]
    list_filter = ['manufacturer', 'category', 'model']
    search_fields = ['serial', 'tag_no']

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [('Category Information: ', {'fields': ['category', 'manufacturers']})]
    list_display = ['category']
    filter_horizontal = ['manufacturers',]
    list_filter = ['manufacturers',]

class ModelAdmin(admin.ModelAdmin):
    fieldsets = [('Model Information: ', {'fields': ['manufacturer', 'category', 'model']})]
    list_display = ['model', 'category', 'manufacturer']
    list_filter = ['category', 'manufacturer']

admin.site.register(SpecList)
admin.site.register(SpecInfo, SpecInfoAdmin)
admin.site.register(Manufacturer)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Item, ItemAdmin)