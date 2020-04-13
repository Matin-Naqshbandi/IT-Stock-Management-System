from django.contrib import admin
from .models import (Employee,
                    Province,
                    Site,
                    Department,
                    Position)
from reversion.admin import VersionAdmin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.

class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Organizational Information'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin, VersionAdmin, ImportExportModelAdmin):
    inlines = (EmployeeInline, )
    list_display = ('username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser','date_joined', 'last_login')
    list_select_related = ('employee', )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

class EmployeeAdmin(VersionAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    fieldsets = [ ('Employee Information', {'fields': ['user', 'province', 'site', 'department','position','hire_date','contract']})]
    list_display = [ 'user','department','position', 'province','site', 'hire_date', 'contract','is_hired_recently', 'timeuntil_out_of_contract']
    list_filter = ['department', 'position']
    # search_fields = ['first_name', 'last_name']
    date_hierarchy = 'hire_date'
    change_list_template = "admin/change_list.html"



admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Province)
admin.site.register(Site)
admin.site.register(Department)
admin.site.register(Position)