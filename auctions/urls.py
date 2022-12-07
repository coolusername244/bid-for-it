from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/leave_comment", views.leave_comment, name="leave_comment"),
    path("listing/<int:listing_id>/add_to_wishlist", views.add_to_wishlist, name="add_to_wishlist"),
    path("listing/<int:listing_id>/remove_from_wishlist", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("listing/<int:listing_id>/place_bid", views.place_bid, name="place_bid"),
]
