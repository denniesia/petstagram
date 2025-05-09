from django.shortcuts import render, redirect, resolve_url
from petstagram.photos.models import Photo
from petstagram.common.models import Like
from petstagram.common.forms import CommentForm
from pyperclip import copy
# Create your views here.
def home_page(request):
    all_photos = Photo.objects.all()
    comment_form = CommentForm()
    context = {
        'all_photos': all_photos,
        'comment_form': comment_form,
    }

    return render(request, 'common/home-page.html', context)


def likes_functionality(request, photo_id: int):
    liked_object = Like.objects.filter(
        to_photo_id=photo_id
    ).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_photo_id=photo_id)
        like.save()

    # the url where the request came from + photo id
    return redirect(request.META.get('HTTP_REFERER')+f'#{photo_id}')
    #open the page again, but focus it on the photo with the same photo id

def share_functionality(request, photo_id: int):
    copy(request.META.get('HTTP_HOST') + resolve_url('photo-details', photo_id))
    # HTTP_HOST = http://127.0.0.1/ + photos/<int:pk>/ -> http://127.0.0.1/photos/<int:pk>/

    return redirect(request.META.get('HTTP_REFERER')+f'#{photo_id}')


def comment_functionality(request, photo_id: int):
    if request.method == 'POST':
        photo = Photo.objects.get(id=photo_id)
        form = CommentForm(request.POST) #we dont get a photo id, it comes from the path

        if form.is_valid():
           comment = form.save(commit=False) #we have to make the relation to the photo, the comment is saved, but not in the database (commit=False)
           comment.to_photo = photo #relation to the photo
           comment.save()

        return redirect(request.META.get('HTTP_REFERER')+f'#{photo_id}')