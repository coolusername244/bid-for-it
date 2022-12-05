from django.contrib import admin

from .models import Category, Listing

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "friendly_name",
    )

class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "price",
        "category",
        "user"
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)