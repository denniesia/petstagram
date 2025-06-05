from django.shortcuts import render
from django.views.generic import CreateView

from django.contrib.auth import get_user_model, login
from django.urls import reverse_lazy
from .forms import AppUserCreationForm
# Create your views here.

UserModel = get_user_model()


# def login(request):
#     return render(request, 'accounts/login-page.html')

class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('home')

#after the reg the user would be loged-in
#after the form is valid
    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

        return response



def profile_delete(request, pk):
    return render(request, 'accounts/profile-delete-page.html')

def profile_details(request, pk):
    return render(request, 'accounts/profile-details-page.html')

def profile_edit(request, pk):
    return render(request, 'accounts/profile-edit-page.html')