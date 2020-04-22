from django.shortcuts import render, redirect #iserrano2
from django.http import HttpResponse
from share.models import Script
#iserrano2 - authentication, login, logout
from django.contrib.auth import authenticate, login, logout
#iserrano2 - import all models created
from .models import Script, Problem, Coder
#iserrano2 - import User model
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404 #iserrano4
from .models import Media, Post, Comment

# s3Integration
import os, json, boto3
from .forms import *
from django.conf import settings

# from django.core.files.storage import FileSystemStorage
from django.template import RequestContext, Template
from custom_storages import MediaStorage



# Create your views here.

#iserrano3
def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            all_posts = Post.objects.all()   # all_problems is a list object [   ]

            return render(request, "share/index.html")
            # return render(request, "share/index.html", {"user":user, "all_posts": all_posts})
        else:
            return redirect("share:login")
    else:
        return HttpResponse(status=500)

#iserrano2
def signup(request):
    if request.user.is_authenticated:
        return redirect("share:index")
    return render(request, 'share/signup.html')

#iserrano2
def create(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # coder_yet = request.POST.get('coder_yet_checkbox')

        if username is not None and email is not None and password is not None: # checking that they are not None
            if not username or not email or not password: # checking that they are not empty
                return render(request, "share/signup.html", {"error": "Please fill in all required fields"})
            if User.objects.filter(username=username).exists():
                return render(request, "share/signup.html", {"error": "Username already exists"})
            elif User.objects.filter(email=email).exists():
                return render(request, "share/signup.html", {"error": "Email already exists"})
            # save our new user in the User model
            user = User.objects.create_user(username, email, password)
            # coder = Coder.objects.create(user= user, coder_yet = coder_yet).save()
            user.save()

            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            # this logs in our new user, backend means that we are using the  Django specific auhentication and not 3rd party

        return redirect("share:index")

    else:
        return redirect("share:signup")

#iserrano2
def login_view(request):
    if request.user.is_authenticated:
        return redirect("share:index")
    return render(request, 'share/login.html')

#iserrano2
# the function loguser is called from the login form
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if not username or not password:
            return render(request, "share/login.html", {"error":"One of the fields was empty"})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("share:index")
        else:
            return render(request, "share/login.html", {"error":"Wrong username or password"})
    else:
        return redirect("share:index")

#iserrano2
def logout_view(request):
    logout(request)
    return redirect("share:login")



#iserrano3
def dashboard(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            my_problems = Problem.objects.filter(coder=user.coder.id)
            my_scripts =  Script.objects.filter(coder=user.coder.id)

            return render(request, "share/dashboard.html", {"my_scripts": my_scripts, "my_problems": my_problems })

def user_profile(request):
    pass

#iserrano4
def edit_profile(request, user_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login", {"user":user, "error":"Please Login"})

        #button is pressed, retrieve user information
        user_info = get_object_or_404(User, pk=user_id)

        #make sure the logged in user is the correct one
        if user_info.id == user.id:
            return render(request, "share/edit_profile.html", {"user_info":user_info})
        else:
            return render(request, "share/login.html",
            {"Error": "Please login to edit profile"})

#iserrano4
def update_profile(request, user_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)

        user_info = get_object_or_404(User, pk=user_id)

        if not request.POST['Username'] or not request.POST['Email'] or not request.POST['Password']:
            return render(request, "share/edit_profile.html", {"user_info":user_info, "Error":"Fill out required fields"})

        else:
            #figure out how to get icon change option
            first_name = request.POST['First Name']
            last_name = request.POST['Last Name']
            username = request.POST['Username']
            email = request.POST['Email']
            password = request.POST['Password']
            bio = request.POST['Bio']

        if user_info.user.id == user.id:
            User.objects.filter(pk=user_id).update(first_name=first_name, last_name=last_name, username=username, email=email, password=password, bio=bio)
        else:
            return render(request, "share/edit_profile.html", {"error":"Unable to update profile"})

#iserrano4
def delete_profile(request, user_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)

        user_info = get_object_or_404(User, pk=user_id)

        if user_info.id == user.id:
            User.objects.get(pk=user_id).delete()
            return redirect("share/signup.html")
        else:
            return render(request, "share/edit_profile.html", {"user":user, "error": "Unable to delete account"})

    else:
        return HttpResponse(status=500)

#iserrano4
def show_post(request, post_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login", {"user":user, "error":"Please Login"})
        else:
            post = get_object_or_404(Post, pk=post_id)

            comments = Comment.objects.filter(post=post_id)
            user_comment = Comment.objects.filter(user=user.id).filter(post=post.id)

        return render(request, "share/post.html", {"user":user, "post":post})

#iserrano4
def publish_post(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login", {"user":user, "error":"Please Login"})
        else:
            return render(request, "share/publish_post_form.html", {"user":user})

#iserrano4
def create_post(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login", {"user":user, "error":"Please Login"})

        # user_id = user.id
        # media_upload=request.FILES['Media']
        # print(media_upload.name)
        # print(media_upload.size)

        # if video == 'on':
        #     video=True
        # else:
        #     video=False

        # post_title = request.POST["title"]
        # post_body = request.POST["description"]
        # the_photo = request.FILES["myphoto"]

        post_title = request.POST.get("title")
        post_body = request.POST.get("description")
        the_photo = request.FILES.get("myphoto")

        # create Photo object
        photo = Photo.objects.create(user = user, photo = the_photo)

        # get photo id
        # photo_id = photo.pk

        # if not post_title and not post_body and not media_upload:
        if not post_title and not post_body and not photo:
            return render(request, "share/publish_post_form.html", {"error":"Please fill in at least one field"})

        try:
            # post = Post.objects.create(user=user, post_title=post_title, post_body=post_body, media_upload=media_upload, photo=photo_id)
            post = Post.objects.create(user=user, post_header=post_title, post_body=post_body, photo=photo)
            photo.save()
            post.save()

            # post = get_object_or_404(Post, pk=post_id)

            # return render(request, "share/dashboard.html", {"user":user, "post":post})
            return render(request, "share/dashboard.html")


        except:
            return render(request, "share/publish_post_form.html", {"error":"Unable to publish post at this time"})

    else:
        user=request.user
        all_posts = Post.objects.all()
        return render(request, "share/index.html", {"user":user, "error":"Unable to create a post at this time"})
        # return render(request, "share/index.html", {"user":user, "all_posts":all_posts, "error":"Unable to create a post at this time"})

#iserrano4
def edit_post(request, post_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login", {"user":user, "error":"Please Login"})

        post = get_object_or_404(Post, pk=post_id)

        if post.user.id == user.id:
            return render(request, "share/edit_post.html", {"post":post})
        else:
            return render(request, "share/dashboard.html", {"error": "Non-authorized user;Unable to edit post"})

#iserrano4
def update_post(request, post_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login", {"user":user, "error":"Please Login"})

        post = get_object_or_404(Post, pk=post_id)

        if not request.POST["Title"] and not request.POST["Description"] and not request.POST["Media"]:
            return render(request, "share/edit_post.html", {"error":"Please fill in at least one field"})
        else:
            media_upload=request.FILES['Media']
            print(media_upload.name)
            print(media_upload.size)

            if video == 'on':
                video=True
            else:
                video=False

            post_title = request.POST["Title"]
            post_body = request.POST["Description"]

        if post.user.id == user.id:
            Post.object.filter(pk=post_id).update(post_title=post_title, post_body=post_body, media_upload=media_upload)
        else:
            return render(request, "share/edit_post.html", {"error":"Unable to update post"})

#iserrano4
def delete_post(request, post_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login", {"user":user, "error":"Please Login"})

        post = get_object_or_404(Post, pk=post_id)

        if post.user.id == user.id:
            Post.object.get(pk=post_id).delete()
            return render(request, "share/user_profile.html")
        else:
            return render(request, "share/dashboard.html", {"error": "Non-authorized user; Unable to delete post"})

#iserrano4
def create_comment(request):
    pass

# s3Integration
def upload(request):
    if request.method == "POST" and request.FILES['myphoto']:
        # title = request.POST['title']
        myphoto = request.FILES['myphoto']
        user = request.user

        photo = Photo.objects.create(user = user, photo = myphoto)

        # save file to AWS
        # media_storage = MediaStorage()

        uploaded_file_url = photo.photo

        #save file to DB
        photo.save()

        photo_id = photo.pk

        # uploaded_file_url = media_storage.url(filename)
        return render(request, 'share/upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'photo_id': photo_id
        })

    return render(request, 'share/upload.html')