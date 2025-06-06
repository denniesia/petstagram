from django.shortcuts import render, redirect, resolve_url
from petstagram.photos.models import Photo
from petstagram.common.models import Like
from petstagram.common.forms import CommentForm, SearchForm
from pyperclip import copy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required

class HomePage(ListView):
    model = Photo
    template_name = 'common/home-page.html'
    context_object_name = 'all_photos' #by degault is object_list
    paginate_by = 5


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comment_form'] = CommentForm()
        context['search_form'] = SearchForm(self.request.GET)
        user = self.request.user

        for photo in context['all_photos']:
            photo.has_liked = photo.like_set.filter(user=user).exists() if user.is_authenticated else False

        return context

    # adding the functionality of the searchbar
    def get_queryset(self):
        queryset = super().get_queryset()
        pet_name = self.request.GET.get('pet_name')

        if pet_name:
            queryset = queryset.filter(
                tagged_pets__name__icontains= pet_name
            )
        return queryset


# def home_page(request):
#     all_photos = Photo.objects.all()
#     comment_form = CommentForm()
#     search_form = SearchForm(request.GET)
#
#     if search_form.is_valid():
#         all_photos = all_photos.filter(
#             tagged_pets__name__icontains=search_form.cleaned_data['pet_name']
#         )
#     photos_per_page = 1
#     paginator = Paginator(all_photos, photos_per_page)
#     page_number = request.GET.get('page')
#     all_photos = paginator.get_page(page_number)
#
#     try:
#         all_photos = paginator.page(page_number)
#     except PageNotAnInteger:
#         all_photos = paginator.page(1)
#     except EmptyPage:
#         all_photos = paginator.page(paginator.num_pages)
#
#
#     context = {
#         'all_photos': all_photos,
#         'comment_form': comment_form,
#         'search_form': search_form,
#     }
#
#     return render(request, 'common/home-page.html', context)

@login_required
def likes_functionality(request, photo_id: int):
    liked_object = Like.objects.filter(
        to_photo_id=photo_id,
        user= request.user
    ).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_photo_id=photo_id, user=request.user)
        like.save()

    # the url where the request came from + photo id
    return redirect(request.META.get('HTTP_REFERER')+f'#{photo_id}')
    #open the page again, but focus it on the photo with the same photo id

def share_functionality(request, photo_id: int):
    copy(request.META.get('HTTP_HOST') + resolve_url('photo-details', photo_id))
    # HTTP_HOST = http://127.0.0.1/ + photos/<int:pk>/ -> http://127.0.0.1/photos/<int:pk>/

    return redirect(request.META.get('HTTP_REFERER')+f'#{photo_id}')


@login_required
def comment_functionality(request, photo_id: int):
    if request.method == 'POST':
        photo = Photo.objects.get(id=photo_id)
        form = CommentForm(request.POST) #we dont get a photo id, it comes from the path

        if form.is_valid():
           comment = form.save(commit=False) #we have to make the relation to the photo, the comment is saved, but not in the database (commit=False)
           comment.to_photo = photo #relation to the photo
           comment.user = request.user
           comment.save()

        return redirect(request.META.get('HTTP_REFERER')+f'#{photo_id}')