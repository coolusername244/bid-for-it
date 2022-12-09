from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef

from .models import User, Listing, Comment, Wishlist, Bid, Category
from .forms import ListingForm, CommentForm, BidForm


def index(request):

    category = None
    category_friendly = None

    # check if user has selected a category to view
    if 'category' in request.GET:
        category = request.GET["category"]
        listings = Listing.objects.filter(category__name=category)
        category_friendly = Category.objects.get(name=category).get_friendly_name()
    # if not, return all listings
    else:
        listings = Listing.objects.all()

    # update current price if bid deleted in django admin
    for listing in listings:
        bids = Bid.objects.filter(listing=listing.id)   
        if bids:
            highest_bid = Bid.objects.filter(listing=listing.id).latest('bid')
            Listing.objects.filter(pk=listing.id).update(current_price=highest_bid.bid)
        else:
            Listing.objects.filter(pk=listing.id).update(current_price=listing.price)

    context = {
        "category": category_friendly,
        "listings": listings,
    }
    return render(request, "auctions/index.html", context)


def listing(request, listing_id):

    # Get selected listing
    listing = Listing.objects.get(pk=listing_id)
    
    # Supply comment form and get any existing comments
    comment_form = CommentForm()
    comments = Comment.objects.filter(listing=listing_id)

    # Supply bid form and any bids for the current listing
    bid_form = BidForm()
    bids = Bid.objects.filter(listing=listing_id)
    if bids:
        highest_bid = Bid.objects.filter(listing=listing_id).latest('bid')
    else:
        highest_bid = None

    # Check if listing is in users wishlist
    wishlist = Listing.objects.filter(
        Exists(Wishlist.objects.filter(
            listing_id=OuterRef("id")
        ))
    )

    context = {
        "listing": listing,
        "comment_form": comment_form,
        "comments": comments,
        "wishlist": wishlist,
        "bid_form": bid_form,
        "bids": bids,
        "highest_bid": highest_bid
    }

    return render(request, "auctions/listing.html", context)


def closed_listings(request):

    # Get all listings that are not active
    listings = Listing.objects.exclude(is_active=True)
    
    context = {
        "listings": listings
    }
    return render(request, "auctions/closed_listings.html", context)


@login_required
def close_listing(request, listing_id):

    # Update listing active status
    Listing.objects.filter(pk=listing_id).update(is_active=False)
    messages.info(request, "Listing closed, no more bids will be accepted")
    return HttpResponseRedirect(
        reverse("listing", args=[listing_id])
    )


@login_required
def delete_listing(request, listing_id):

    # Delete listing from database and return user to all listings
    Listing.objects.filter(pk=listing_id).delete()
    messages.success(request, "Your listing has been deleted")
    return HttpResponseRedirect(
        reverse("index")
    )


@login_required
def place_bid(request, listing_id):

    # Get current listing and check for bids
    listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.filter(listing=listing_id).count()
    bid = request.POST["bid"]
    form = BidForm(request.POST)
    if bids:
        highest_bid = Bid.objects.filter(listing=listing_id).latest('bid')
    else:
        highest_bid = None

    # function to update the highest bid on listing
    def update_bids(request):
        if form.is_valid():
            form.instance.user = request.user
            form.instance.listing = listing
            Listing.objects.filter(pk=listing_id).update(current_price=bid)
            form.save()
    
    # if there are no bids, check bid is higher than listing price
    if not bids:
        if int(bid) >= int(listing.price):
            update_bids(request)
            messages.success(request, "Bid placed successfully!")
            return HttpResponseRedirect(
                reverse("listing", args=[listing_id])
            )
        else:
            messages.warning(
                request, 
                f"Your bid (${bid}) is lower than the listing price (${listing.price})"
            )
            return HttpResponseRedirect(
                reverse("listing", args=[listing_id])
            )
    # if there are bids, check users bid is higher than current highest
    else:
        if int(bid) > int(highest_bid.bid):
            update_bids(request)
            messages.success(request, "Bid placed successfully!")
            return HttpResponseRedirect(
                reverse("listing", args=[listing_id])
            )
        else:
            messages.warning(
                request, 
                f"Your bid is lower than the current bid (${highest_bid.bid})"
            )
            return HttpResponseRedirect(
                reverse("listing", args=[listing_id])
            )


@login_required
def leave_comment(request, listing_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        listing = Listing.objects.get(pk=listing_id)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.listing = listing
            form.save()
            messages.success(request, "You commented on this item")
            return HttpResponseRedirect(
                reverse("listing", args=[listing_id])
            )
        else:
            messages.error(request, "Error leaving comment, please try again")
            return HttpResponseRedirect(
                reverse("listing", args=[listing_id])
            )


@login_required
def add_to_wishlist(request, listing_id):

    # Create instance for database and save to users wishlist
    instance = Wishlist.objects.create(
        user = request.user,
        listing = Listing.objects.get(pk=listing_id)
    )
    instance.save()
    return HttpResponseRedirect(
        reverse("listing", args=[listing_id])
    )


@login_required
def remove_from_wishlist(request, listing_id):

    # Get listing from users wishlist and delete
    Wishlist.objects.filter(
        user= request.user,
        listing = Listing.objects.get(pk=listing_id)
    ).delete()
    return HttpResponseRedirect(
        reverse("listing", args=[listing_id])
    )


@login_required
def wishlist(request):

    # Get all listings in the users wishlist and present
    wishlist = Listing.objects.filter(
        Exists(Wishlist.objects.filter(
            listing_id=OuterRef("id")
        ))
    )
    context = {
        "wishlist": wishlist
    }
    return render(request, "auctions/wishlist.html", context)


@login_required
def create(request):

    # Get form data, chcek and create database instance if valid
    if request.method == "POST":
        form = ListingForm(request.POST)
           
        if form.is_valid():
            form.instance.user = request.user
            form.instance.current_price = request.POST['price']
            form.save()
            messages.success(request, "Item successfully registered!")
            return HttpResponseRedirect(reverse("index"))
        
        # return form to user to correct if not valid
        # custom checks have been created in models.py
        else:
            context = {
                "form": form
            }
            return render(request, "auctions/create.html", context)
    
    # Present user with the listing form
    else:
        # set initial category and condition to "Please Select"
        form = ListingForm(
            initial={
                "category": "14",
                "condition": "1" 
            }
        )
        context = {
            "form": form
        }
        return render(request, "auctions/create.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {username}!")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username and/or password")
            return render(request, "auctions/login.html")
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out. See you next time!")
        return HttpResponseRedirect(reverse("index"))
    else:
        messages.success(request, "You were not logged in!")
        return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Passwords must match")
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken")
            return render(request, "auctions/register.html")
        login(request, user)
        messages.success(request, f"Account successfully registered! Welcome {user.username}")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
