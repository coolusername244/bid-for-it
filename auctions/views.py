from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comment
from .forms import ListingForm, CommentForm


def index(request):
    listings = Listing.objects.all()

    context = {
        "listings": listings
    }
    return render(request, "auctions/index.html", context)


def listing(request, listing_id):

    listing = Listing.objects.get(pk=listing_id)
    comment_form = CommentForm()
    comments = Comment.objects.filter(listing=listing_id)

    context = {
        "listing": listing,
        "comment_form": comment_form,
        "comments": comments
    }

    return render(request, "auctions/listing.html", context)


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
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
           
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, "Item successfully registered!")
            return HttpResponseRedirect(reverse("index"))
        else:
            context = {
                "form": form
            }
            return render(request, "auctions/create.html", context)
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


@login_required
def wishlist(request):
    return render(request, "auctions/wishlist.html")


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
