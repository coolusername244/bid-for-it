from django.contrib import admin

from .models import Category, Listing, User, Condition

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username"
    )

class ConditionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "friendly_name",
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
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


admin.site.register(Condition, ConditionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(User, UserAdmin)