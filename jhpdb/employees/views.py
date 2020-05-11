from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def index_view(request):
	return render(request, "portal/index.html")

def not_found_view(request):
    return render(request, "portal/404.html")
@login_required
def extension_numbers_view(request):
    return render(request, 'portal/extension_numbers.html')
@login_required
def personal_contacts_view(request):
    return render(request, 'portal/personal_contacts.html')

def custom_view(request):
    return render(request, 'dist/index.html')