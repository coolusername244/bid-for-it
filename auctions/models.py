from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# category select validator
def category_check(value):
    # 14 = Please Select
    if value == 14:
        raise ValidationError(
            _('Please select a category'),
            params={'value': value},
        )

def condition_check(value):
    # 1 = Please Select
    if value == 1:
        raise ValidationError(
            _('Please select a condition'),
            params={'value': value},
        )

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


class Condition(models.Model):
    name = models.CharField(max_length=254, null=False)
    friendly_name = models.CharField(max_length=254, null=False)

    def __str__(self):
        return f"{self.name}"
    
    def get_friendly_name(self):
        return self.friendly_name


class Listing(models.Model):
    title = models.CharField(max_length=254)
    subtitle = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(1)])
    category = models.ForeignKey("Category", null=True, on_delete=models.SET_NULL, validators=[category_check])
    condition = models.ForeignKey("Condition", null=True, on_delete=models.SET_NULL, validators=[condition_check])
    image_url = models.URLField()
    created = models.DateTimeField(default=timezone.now, editable=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        return f"Item: {self.title} - Seller: {self.user}"