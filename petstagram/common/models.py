from django.db import models
from petstagram.photos.models import Photo
from django.contrib.auth import get_user_model
# Create your models here.

UserModel = get_user_model()

class Comment(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['date_time_of_publication']),
        ] # so the ordering would be faster
        ordering = ['-date_time_of_publication']

    text = models.TextField(
        max_length=300,

    )
    date_time_of_publication = models.DateTimeField(auto_now_add=True)
    to_photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,

    )


class Like(models.Model):
    to_photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,

    )