from django.contrib import admin

from .models import Category, Listing, User, Condition, Comment, Bid

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
        "is_active",
        "price",
        "current_price",
        "category",
        "user"
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "listing",
        "user",
        "date"
    )


class BidAdmin(admin.ModelAdmin):
    list_display = (
        "listing",
        "user",
        "bid",
        "date",
    )


admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Bid, BidAdmin)