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
    # This will help you to disable change functionality
    def has_add_permission(self, request, obj=None):
        return False

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [('Category Information: ', {'fields': ['name', 'manufacturers']})]
    list_display = ['name']
    filter_horizontal = ['manufacturers',]
    list_filter = ['manufacturers',]

class ModelAdmin(admin.ModelAdmin):
    fieldsets = [('Model Information: ', {'fields': ['manufacturer', 'category', 'name', 'item_count', 'expendable']})]
    list_display = ['name', 'category', 'manufacturer', 'item_count', 'item_in_stock', 'item_assigned', 'item_expended','item_lost', 'item_damaged', 'expendable']
    list_filter = ['category', 'manufacturer', 'expendable']

class ItemAssignAdmin(admin.ModelAdmin):
    fieldsets = [ ('Item Assign history: ', {'fields': ['item', 'assign_to','assign_status']})]
    list_display = ['item','assign_to', 'assign_by', 'assigned_date','received_date','received_by', 'assign_status']
    list_filter = ['assigned_date', 'received_date',]
    date_hierarchy = 'received_date'
    raw_id_fields = ('item','assign_to')
    exclude = ('assign_by', 'received_by',)
    #only Assign items when Assign is selected as ItemAssign Status
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