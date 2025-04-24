from django.db import models

# Create your models here.
class Pet(models.Model):
    name = models.CharField(max_length=30)
    personal_photo = models.URLField()
    date_of_birth = models.DateField(blank=True, null=True)
    slug = models.SlugField(null=True, blank=True, unique=True, editable=False)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) #it is called twice, to get the id first and then to save the combination with self.name
        if not self.slug:
            self.slug = slugify((f"{self.name}-{self.id}"))
        super().save(*args, **kwargs)