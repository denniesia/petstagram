from django.db import models
from django.core.validators import MinLengthValidator
from petstagram.pets.models import Pet
from .validators import FileSizeValidator
from django.contrib.auth import get_user_model
# Create your models here.

UserModel = get_user_model()

class Photo(models.Model):
    photo = models.ImageField(
        upload_to='',
        validators=[
            FileSizeValidator(5)
        ]
    )
    description = models.TextField(
        max_length=300,
        validators=[
            MinLengthValidator(10)
        ],
        blank=True,
        null=True
    )
    location = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )
    tagged_pets = models.ManyToManyField(Pet, blank=True)
    date_of_publication = models.DateField(
        auto_now_add=True,
    )
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,

    )