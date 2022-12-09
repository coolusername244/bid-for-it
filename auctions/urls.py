from django.urls import path

from . import views

urlpatterns = [

    # index urls
    path("", views.index, name="index"),

    # user urls
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # listing urls
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("listing/<int:listing_id>/place_bid", views.place_bid, name="place_bid"),
    path("listing/<int:listing_id>/close_listing", views.close_listing, name="close_listing"),
    path("listing/<int:listing_id>delete_listing", views.delete_listing, name="delete_listing"),
    
    # wishlist urls
    path("wishlist", views.wishlist, name="wishlist"),
    path("listing/<int:listing_id>/add_to_wishlist", views.add_to_wishlist, name="add_to_wishlist"),
    path("listing/<int:listing_id>/remove_from_wishlist", views.remove_from_wishlist, name="remove_from_wishlist"),

    # comment urls
    path("listing/<int:listing_id>/leave_comment", views.leave_comment, name="leave_comment"),
]
