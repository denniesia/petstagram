from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import AppUserCreationForm, ProfileEditForm
from .models import Profile
from django.shortcuts import get_object_or_404

from django.db.models.aggregates import Count


UserModel = get_user_model()


class AppUserLoginView(LoginView):
    template_name = 'accounts/login-page.html'

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



class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('login')

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        photos_with_likes = self.object.photo_set.annotate(likes_count=Count('like'))
        context['total_likes_count'] = sum(photo.likes_count for photo in photos_with_likes)
        context['total_pets'] = self.object.pet_set.count()
        context['total_photos_count'] = self.object.photo_set.count()

        return context

class ProfileEditView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})