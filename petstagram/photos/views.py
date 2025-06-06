from django.shortcuts import render, redirect
from petstagram.photos.models import Photo
from petstagram.photos.forms import PhotoAddForm, PhotoEditForm
from petstagram.common.forms import CommentForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Create your views here.

class PhotoAddView(LoginRequiredMixin, CreateView): #support File Handling in get_form_kwargs()
    model = Photo
    template_name = 'photos/photo-add-page.html'
    form_class = PhotoAddForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.user = self.request.user
        photo.save() #because of the many to many field
        #form.save_m2m()
        return super().form_valid(form)


# def photo_add_page(request):
#     form = PhotoAddForm(request.POST or None, request.FILES or None)
#
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#     context = {
#         "form": form,
#     }
#     return render(request, 'photos/photo-add-page.html', context)

class PhotoDetailsView(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = 'photos/photo-details-page.html'
    context_object_name = 'photo' # default photo or obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['likes'] = self.object.like_set.all()
        context['comments'] = self.object.comment_set.all()
        context['comment_form'] = CommentForm()
        self.object.has_liked = self.object.like_set.filter(user=self.request.user).exists()
        return context

# @login_required()
# def photo_details_page(request, pk):
#     photo = Photo.objects.get(pk=pk)
#     likes = photo.like_set.all()
#     comments = photo.comment_set.all()
#
#     comment_form = CommentForm()
#
#     context = {
#         'photo': photo,
#         'likes': likes,
#         'comments': comments,
#         'comment_form': comment_form,
#     }
#     return render(request, 'photos/photo-details-page.html', context)

@login_required()
def photo_delete(request, pk):
    photo = Photo.objects.get(pk=pk)

    if request.user == photo.user:
        Photo.objects.get(pk=pk).delete()

    return redirect('home')


class PhotoEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Photo
    form_class = PhotoEditForm
    template_name = 'photos/photo-edit-page.html'

    def test_func(self):
        photo = get_object_or_404(Photo, pk=self.kwargs['pk'])
        return self.request.user == photo.user

    def get_success_url(self):
        return reverse_lazy(
            'photo-details',
            kwargs={'pk': self.object.pk}
        )
# def photo_edit_page(request, pk):
#     photo = Photo.objects.get(pk=pk)
#     form = PhotoEditForm(request.POST or None, instance=photo)
#
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('photo-details', pk)
#
#     context = {
#         "form": form,
#         "photo": photo,
#     }
#
#     return render(request, 'photos/photo-edit-page.html', context)