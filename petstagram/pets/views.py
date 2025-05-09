from django.shortcuts import render, redirect
from petstagram.pets.models import Pet
from petstagram.pets.forms import PetAddForm, PetEditForm, PetDeleteForm
from petstagram.common.forms import CommentForm

# Create your views here.
def pet_add_page(request):
    form = PetAddForm(request.POST or None)

    if request.method =="POST":
        if form.is_valid():
            form.save()
            return redirect('profile-details', pk=1)

    context = {
        "form": form,
    }

    return render(request, 'pets/pet-add-page.html', context)

def pet_edit_page(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    form = PetEditForm(request.POST or None, instance=pet) #instance, so that the data is already filled

    if request.method =="POST":
        if form.is_valid():
            form.save()
            return redirect('details-pet', username, pet_slug)

    context = {
        "form": form,
        "pet": pet,
    }

    return render(request, 'pets/pet-edit-page.html', context)


def pet_details_page(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug) #unique identifier
    all_photos = pet.photo_set.all()

    comment_form = CommentForm()

    context = {
        'pet': pet,
        'all_photos': all_photos,
        'comment_form': comment_form,

    }
    return render(request, 'pets/pet-details-page.html', context)

def pet_delete_page(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    form = PetDeleteForm(instance=pet) # the user does not fill in data, thats why we dont need a POST method

    if request.method =="POST":
        pet.delete()
        return redirect('profile-details', pk=1)
    context = {
        "form": form,
        "pet": pet,
    }
    return render(request, 'pets/pet-delete-page.html', context)




