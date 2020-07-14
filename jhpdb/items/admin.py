from django.contrib import admin
from .models import (
    SpecList, SpecInfo, Item, Category, Manufacturer, Model, ItemAssign, PersonalDevice, SpecList, Manufacturer
)
from django.utils import timezone
from reversion.admin import VersionAdmin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class SpecInfoAdmin(VersionAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    fieldsets = [('Specs Information: ', {'fields': ['item', 'spec', 'info']})]
    list_display = ['item', 'spec', 'info']
    list_filter = ['spec', 'item']
    search_fields = ['info',]
    change_list_template = "admin/change_list.html"

class SpecInfoInline(admin.TabularInline):
    model = SpecInfo
    extra = 1

class SpecListAdmin(VersionAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    fieldsets = [('Specs List Information: ', {'fields': ['name',]})]
    list_display = ['name', ]
    search_fields = ['name',]
    change_list_template = "admin/change_list.html"

class ItemAdmin(VersionAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    fieldsets = [ ('Item Information: !!DO NOT ENTER USING ADMIN!!', {'fields': ['manufacturer', 'category', 'model','serial','tag_no', 'note',]})]
    list_display = ['model', 'serial', 'tag_no', 'category', 'manufacturer', 'status', 'has_note']
    inlines = [SpecInfoInline]
    list_filter = ['manufacturer', 'category', 'model',]
    search_fields = ['serial', 'tag_no']
    change_list_template = "admin/change_list.html"
    # This will help you to disable add functionality
    def has_add_permission(self, request, obj=None):
        return False

class ManufacturerAdmin(VersionAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    fieldsets = [ ('Manufacturer Information', {'fields': ['name']})]
    list_display = ('name', )
    search_fields = ['name', ]
    change_list_template = "admin/change_list.html"

class CategoryAdmin(VersionAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    fieldsets = [('Category Information: ', {'fields': ['name', 'manufacturers']})]
    list_display = ['name', 'get_manufacturers']
    filter_horizontal = ['manufacturers',]
    list_filter = ['manufacturers',]
    search_fields = ['name',]
    change_list_template = "admin/change_list.html"

    def get_manufacturers(self, obj):
        return ", ".join([m.name for m in obj.manufacturers.all()])

class ModelAdmin(VersionAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    fieldsets = [('Model Information: ', {'fields': ['manufacturer', 'category', 'name', 'item_count', 'expendable']})]
    list_display = ['name', 'category', 'manufacturer', 'item_count', 'item_in_stock', 'item_assigned', 'item_expended','item_lost', 'item_damaged', 'expendable']
    list_filter = ['category', 'manufacturer', 'expendable']
    search_fields = ['name',]
    change_list_template = "admin/change_list.html"

class ItemAssignAdmin(VersionAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    fieldsets = [ ('Item Assign history: ', {'fields': ['item', 'assign_to','assign_status']})]
    list_display = ['item','assign_to', 'assign_by', 'assigned_date','received_date','received_by', 'assign_status']
    list_filter = ['assigned_date', 'received_date',]
    date_hierarchy = 'received_date'
    raw_id_fields = ('item','assign_to')
    exclude = ('assign_by', 'received_by',)
    change_list_template = "admin/change_list.html"

    #only Assign items when Assign is selected as ItemAssign Status
    def save_model(self, request, obj, form, change): 
        if obj.assign_status=='0': 
            obj.assign_by = request.user.employee;
        if obj.assign_status!='0':
            obj.received_by = request.user.employee;
            obj.received_date = timezone.now()
        obj.save()

class PersonalDeviceAdmin(VersionAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    fieldsets = [ ('Employees Personal Device Information: ', {'fields': ['device','mac']})]
    list_display = ['employee','device', 'mac']
    change_list_template = "admin/change_list.html"
    # raw_id_fields = ('employee',)
    # exclude = ('employee',)
    def save_model(self, request, obj, form, change): 
        obj.employee = request.user.employee;
        obj.save()

admin.site.register(SpecList, SpecListAdmin)
admin.site.register(SpecInfo, SpecInfoAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemAssign, ItemAssignAdmin)
admin.site.register(PersonalDevice, PersonalDeviceAdmin)