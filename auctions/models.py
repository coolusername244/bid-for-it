from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    
    def get_friendly_name(self):
        return self.friendly_name

class Listing(models.Model):
    title = models.CharField(max_length=254)
    subtitle = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    category = models.ForeignKey("Category", null=True, on_delete=models.SET_NULL)
    image_url = models.URLField()
    created = models.DateTimeField(default=timezone.now, editable=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        return f"Item: {self.title} - Seller: {self.user}"