from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from petstagram.pets.models import Pet
from petstagram.pets.forms import PetAddForm, PetEditForm, PetDeleteForm
from petstagram.common.forms import CommentForm
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import get_object_or_404
# Create your views here.

class AddPetView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetAddForm
    template_name =  'pets/pet-add-page.html'


    def form_valid(self, form):
        pet = form.save(commit=False)
        pet.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.request.user.id})

# def pet_add_page(request):
#     form = PetAddForm(request.POST or None)
#
#     if request.method =="POST":
#         if form.is_valid():
#             form.save()
#             return redirect('profile-details', pk=1)
#
#     context = {
#         "form": form,
#     }
#
#     return render(request, 'pets/pet-add-page.html', context)

class PetEditView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Pet
    template_name = 'pets/pet-edit-page.html'
    slug_url_kwarg = 'pet_slug'
    form_class = PetEditForm

    def test_func(self):
        pet = get_object_or_404(Pet, slug=self.kwargs['pet_slug'])
        return self.request.user == pet.user

    def get_success_url(self):
        return reverse_lazy(
            'details-pet',
            #kwargs are passed on from the base class View in the def 'setup'
            kwargs={
                'username': self.kwargs['username'],
                'pet_slug': self.kwargs['pet_slug']
            }
        )

# def pet_edit_page(request, username, pet_slug):
#     pet = Pet.objects.get(slug=pet_slug)
#     form = PetEditForm(request.POST or None, instance=pet) #instance, so that the data is already filled
#
#     if request.method =="POST":
#         if form.is_valid():
#             form.save()
#             return redirect('details-pet', username, pet_slug)
#
#     context = {
#         "form": form,
#         "pet": pet,
#     }
#
#     return render(request, 'pets/pet-edit-page.html', context)

class PetDetailsView(LoginRequiredMixin, DetailView):
    model = Pet
    template_name = 'pets/pet-details-page.html'
    slug_url_kwarg = 'pet_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_photos'] = context['pet'].photo_set.all()
        context['comment_form'] = CommentForm()

        all_photos = context['pet'].photo_set.all()

        for photo in all_photos:
            photo.has_liked = photo.like_set.filter(user=self.request.user).exists()

        context['all_photos'] = all_photos
        return context

# def pet_details_page(request, username, pet_slug):
#     pet = Pet.objects.get(slug=pet_slug) #unique identifier
#     all_photos = pet.photo_set.all()
#
#     comment_form = CommentForm()
#
#     context = {
#         'pet': pet,
#         'all_photos': all_photos,
#         'comment_form': comment_form,
#
#     }
#     return render(request, 'pets/pet-details-page.html', context)

class PetDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Pet
    template_name = 'pets/pet-delete-page.html'
    form_class = PetDeleteForm
    slug_url_kwarg = 'pet_slug'

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.request.user.pk})

    def test_func(self):
        pet = get_object_or_404(Pet, slug=self.kwargs['pet_slug'])
        return self.request.user == pet.user

    def get_initial(self) -> dict:
        return self.get_object().__dict__

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'data':self.get_initial(),
        })

        return kwargs


# def pet_delete_page(request, username, pet_slug):
#     pet = Pet.objects.get(slug=pet_slug)
#     form = PetDeleteForm(instance=pet) # the user does not fill in data, thats why we dont need a POST method
#
#     if request.method =="POST":
#         pet.delete()
#         return redirect('profile-details', pk=1)
#     context = {
#         "form": form,
#         "pet": pet,
#     }
#     return render(request, 'pets/pet-delete-page.html', context)




