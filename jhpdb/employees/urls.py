from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (index_view, not_found_view, extension_numbers_view, personal_contacts_view, custom_view)

app_name = 'employees'

urlpatterns = [
    path('', index_view, name='index'),
    path('404/', not_found_view, name='404'),
    path('extension-numbers/', extension_numbers_view, name='extension_numbers'),
    path('personal-contacts/', personal_contacts_view, name='personal_contacts'),
    path('custom/', custom_view, name='custom'),

]