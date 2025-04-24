from django.db import models

# Create your models here.
class Pet(models.Model):
    name = models.CharField(max_length=30)
    personal_photo = models.URLField()
    date_of_birth = models.DateField(blank=True, null=True)
    slug = models.SlugField(null=False, blank=True, unique=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify((f"{self.name}-{self.id}"))
        super().save(*args, **kwargs)