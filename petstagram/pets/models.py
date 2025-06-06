from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model
# Create your models here.


UserModel = get_user_model()

class Pet(models.Model):
    name = models.CharField(max_length=30)
    personal_photo = models.URLField()
    date_of_birth = models.DateField(blank=True, null=True)
    slug = models.SlugField(null=True, blank=True, unique=True, editable=False)
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,

    )


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) #it is called twice, to get the id first and then to save the combination with self.name
        if not self.slug:
            self.slug = slugify((f"{self.name}-{self.id}"))
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name