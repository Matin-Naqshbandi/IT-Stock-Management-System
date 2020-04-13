from django.contrib import admin
from .models import (Employee,
                    Province,
                    Site,
                    Department,
                    Position)
from reversion.admin import VersionAdmin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class EmployeeAdmin(VersionAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    fieldsets = [ ('Employee Information', {'fields': ['province', 'site', 'department','position','hire_date','contract']})]
    list_display = [ 'department','position', 'province','is_hired_recently', 'still_hired']
    list_filter = ['department', 'position']
    date_hierarchy = 'hire_date'
    # search_fields = ['first_name', 'last_name']
    change_list_template = "admin/change_list.html"


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Province)
admin.site.register(Site)
admin.site.register(Department)
admin.site.register(Position)