from django.shortcuts import render

# Create your views here.

def register(request):
    return render(request, 'accounts/register-page.html')

def login(request):
    return render(request, 'accounts/login-page.html')

def profile_delete(request, pk):
    return render(request, 'accounts/profile-delete-page.html')

def profile_details(request, pk):
    return render(request, 'accounts/profile-details-page.html')

def profile_edit(request, pk):
    return render(request, 'accounts/profile-edit-page.html')