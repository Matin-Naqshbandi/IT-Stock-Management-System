from django.contrib import admin
from .models import (
    SpecList, SpecInfo, Item, Category, Manufacturer, Model, ItemAssign
)
from django.utils import timezone

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
    fieldsets = [ ('Item Information: !!DO NOT ENTER USING ADMIN!!', {'fields': ['manufacturer', 'category', 'model','serial','tag_no', 'note',]})]
    list_display = ['model', 'serial', 'tag_no', 'category', 'manufacturer', 'status']
    inlines = [SpecInfoInline]
    list_filter = ['manufacturer', 'category', 'model',]
    search_fields = ['serial', 'tag_no']

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [('Category Information: ', {'fields': ['category', 'manufacturers']})]
    list_display = ['category']
    filter_horizontal = ['manufacturers',]
    list_filter = ['manufacturers',]

class ModelAdmin(admin.ModelAdmin):
    fieldsets = [('Model Information: ', {'fields': ['manufacturer', 'category', 'model', 'expendable']})]
    list_display = ['model', 'category', 'manufacturer', 'expendable']
    list_filter = ['category', 'manufacturer', 'expendable']

class ItemAssignAdmin(admin.ModelAdmin):
    fieldsets = [ ('Item Assign history: ', {'fields': ['item', 'assign_to','assign_status']})]
    list_display = ['item','assign_to', 'assign_by', 'assigned_date','received_date','received_by', 'assign_status']
    list_filter = ['assigned_date', 'received_date',]
    date_hierarchy = 'received_date'
    raw_id_fields = ('item','assign_to')
    exclude = ('assign_by', 'received_by',)
    def save_model(self, request, obj, form, change):
        if obj.assign_status=='0':
            obj.assign_by = request.user.employee;
        if obj.assign_status!='0':
            obj.received_by = request.user.employee;
            obj.received_date = timezone.now()
        obj.save()

admin.site.register(SpecList)
admin.site.register(SpecInfo, SpecInfoAdmin)
admin.site.register(Manufacturer)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemAssign, ItemAssignAdmin)