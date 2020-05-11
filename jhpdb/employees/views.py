from django.shortcuts import render

# Create your views here.

def index_view(request):
	return render(request, "portal/index.html")

def not_found_view(request):
    return render(request, "portal/404.html")

def extension_numbers_view(request):
    return render(request, 'portal/extension_numbers.html')

def personal_contacts_view(request):
    return render(request, 'portal/personal_contacts.html')