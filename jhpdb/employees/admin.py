from django.contrib import admin
from .models import (Employee, Province, Site, Department, Position)
from reversion.admin import VersionAdmin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from simple_history import register

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser','date_joined', 'last_login')

# class EmployeeInline(admin.StackedInline):
#     model = Employee
#     can_delete = False
#     verbose_name_plural = 'Organizational Information'
#     fk_name = 'user'

# class CustomUserAdmin(UserAdmin, VersionAdmin, ImportExportModelAdmin):
#     inlines = (EmployeeInline, )
#     list_display = ('username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser','date_joined', 'last_login')
#     list_select_related = ('employee', )

#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(CustomUserAdmin, self).get_inline_instances(request, obj)

class EmployeeAdmin(VersionAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    fieldsets = [ ('Employee Information', {'fields': ['user', 'province', 'site', 'department','position','hire_date','contract_end_date', ]})]
    list_display = ['user', 'department','position', 'province','site', 'hire_date', 'contract_end_date', 'timeuntil_out_of_contract', 'is_hired_recently' ]
    list_filter = ['department', 'position']
    date_hierarchy = 'hire_date'
    raw_id_fields = ("user",)
    change_list_template = "admin/change_list.html"

class PositionAdmin(VersionAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    fieldsets = [ ('Positions', {'fields': ['department', 'position']})]
    list_display = ('department', 'position')
    change_list_template = "admin/change_list.html"


class DepartmentAdmin(VersionAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    fieldsets = [ ('Departments', {'fields': ['department']})]
    list_display = ('department', )
    change_list_template = "admin/change_list.html"

    
class ProvinceAdmin(VersionAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    fieldsets = [ ('Provinces', {'fields': ['province']})]
    list_display = ('province', )
    change_list_template = "admin/change_list.html"


class SiteAdmin(VersionAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    fieldsets = [ ('Sites', {'fields': ['province', 'site']})]
    list_display = ('province','site')
    change_list_template = "admin/change_list.html"


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Position, PositionAdmin)
# register(User) #for django simple history