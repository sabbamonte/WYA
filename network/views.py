from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import time
from django.core.exceptions import ObjectDoesNotExist

from .models import User, New_Post, Following, Avatar


def index(request):

    # Get all the posts and avatars and paginate the posts, 10 at a time
    all_posts = New_Post.objects.all().order_by('-timestamp')
    all_avatars = Avatar.objects.all()

    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "GET":
        return render(request, "network/index.html", {'page_obj': page_obj, "all_avatars": all_avatars})
    
    else:
        # create a new post when submitted
        post = New_Post()
        post.user = request.user
        print(request.POST['post'])
        if not request.POST['post']:
            return JsonResponse({"error": "You have to write something."}, status=400)
        post.post = request.POST['post']
        post.save()
        return HttpResponseRedirect(reverse("index"))

def login_view(request):
    if request.method == "POST":

        # Try to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    # log user out
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Try to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def profile(request, username):

    # show user's posts, avatar, followers and people you follow on page
    if request.method == "GET":
        user = User.objects.get(username=username)
        current_user = User.objects.filter(username=request.user)
        posts = New_Post.objects.filter(user=user).order_by('-timestamp')
        try: 
            avatar = Avatar.objects.get(user=user.id)
        except ObjectDoesNotExist:
            avatar = None 

        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # find all the people you follow and your followers and create a count for them to send to template
        followings = Following.objects.filter(user=user)
        followers_counter = 0
        followers = []
        following_counter = 0
        all_followings = []
        for following in followings:
            if following.followers is not None:
                followers_counter += 1
                print(following.followers)
                followers.append(following.followers)
            if following.following is not None:
                following_counter += 1
                all_followings.append(following.following)

        # check if it's the current user's profile to toggle different things in HTML template
        same_user = None
        if user in current_user:
            same_user = "same user"

        # check if current user follows this user already 
        all_follows = Following.objects.filter(user=request.user)
        followed = None
        for follow in all_follows:
            if follow.following == user:
                followed = "followed"
        
        return render(request, "network/profile.html", {"page_obj": page_obj, "followed":followed, 
        "followers_counter":followers_counter, "following_counter":following_counter, "followers":followers, 
            "all_followings":all_followings, "user":user, "same_user":same_user, "avatar":avatar})
    
    # delete avatar from profile
    if request.method == "POST" and "delete_photo" in request.POST:
        Avatar.objects.get(user=request.user).delete()
        user = request.user
        return HttpResponseRedirect(reverse("index"))

    # add new avatar to profile
    if request.method == "POST" and "avatar" in request.POST:
        form = request.FILES['file']
        new_avatar = Avatar()
        new_avatar.user = request.user
        new_avatar.avatar = form
        new_avatar.save()
        
        return HttpResponseRedirect(reverse("index"))

    # follow specific user and put current user in follower and following model
    if request.method == "POST" and "follow" in request.POST:
        user = User.objects.get(username=username)

        following = Following()
        following.user = request.user
        following.following = user
        following.save()
        
        follower = Following()
        follower.user = user
        follower.followers = request.user
        follower.save()

        return HttpResponseRedirect(reverse("index"))

    # delete current user from follower and the unfollowed user from the following model
    if request.method == "POST" and "unfollow" in request.POST:
        user = User.objects.get(username=username)

        follower = Following.objects.filter(following=user, user=request.user)
        following = Following.objects.filter(followers=request.user, user=user)
        follower.delete()
        following.delete()

        return HttpResponseRedirect(reverse("index"))

@login_required
def followers(request):

    # show all the people the current user follows
    user = User.objects.get(username=request.user)
    follows = user.followers.all()

    paginator = Paginator(follows, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/followers.html", {"page_obj": page_obj})

@csrf_exempt
@login_required
def edit(request, post_id):

    # get the specific post
    post = New_Post.objects.filter(user=request.user, id=post_id).values()

    if request.method == "GET":
        return JsonResponse({"post": list(post)})

    elif request.method == "PUT":
        # save edited post
        post = New_Post.objects.get(user=request.user, id=post_id)
        data = json.loads(request.body.decode("utf-8"))
        post.post = data.get('post')
        post.save()
        return JsonResponse({"message": "Post updated successfully."}, status=201)

@csrf_exempt
@login_required
def likes(request, post_id,):
    posts = New_Post.objects.filter(id=post_id).values()

    if request.method == "GET":
        return JsonResponse({"posts":list(posts)})

    elif request.method == "PUT":
        # get specific post
        posts = New_Post.objects.get(id=post_id)
        for post in posts.likes.all():
            # if current user in likes, delete from likes
            if request.user == post:
                posts.likes.remove(request.user)
                return JsonResponse({"message": "Post unliked successfully."}, status=201)

        # if current user not in likes, add to likes
        posts.likes.add(request.user)
        return JsonResponse({"message": "Post liked successfully."}, status=201)

@csrf_exempt
@login_required
def count(request, post_id,):
    posts = New_Post.objects.filter(id=post_id).values()
    print(posts)

    if request.method == "GET":
        return JsonResponse({"posts":list(posts)})

    # set the new counter
    elif request.method == "PUT":
        posts = New_Post.objects.get(id=post_id)
        data = json.loads(request.body.decode("utf-8"))
        counter = data.get('counter')

        # set default counter to zero
        if int(counter) < 0:
            counter = 0
        if counter == None:
            counter = 0

        # save new counter
        posts.counter = counter
        posts.save()
        return JsonResponse({"message": "Post liked successfully."}, status=201)

@csrf_exempt
@login_required
def delete(request, post_id):
    if request.method == "DELETE":
        # find specific post and delete from database
        data = json.loads(request.body.decode("utf-8"))
        New_Post.objects.get(id=data.get('id')).delete()
        return JsonResponse({"message": "Post deleted successfully."}, status=201)





        
    
    