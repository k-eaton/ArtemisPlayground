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
from django.shortcuts import get_list_or_404 #iserrano4
from .models import Media, Post, Comment, Photo

# s3Integration
import os, json, boto3
from .forms import *
from django.conf import settings

# from django.core.files.storage import FileSystemStorage
from django.template import RequestContext, Template
from custom_storages import MediaStorage
from .forms import UserUpdateForm, ProfileUpdateForm


# Create your views here.

#iserrano3
def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            all_posts = Post.objects.all()   # all_posts is a list object [   ]

            return render(request, "share/dashboard.html")

        else:
            return redirect("share:login")
    else:
        return HttpResponse(status=500)

#iserrano2
def signup(request):
    if request.user.is_authenticated:
        return redirect("share:dashboard")
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

        return redirect("share:dashboard")

    else:
        return redirect("share:signup")

#iserrano2
def login_view(request):
    if request.user.is_authenticated:
        return redirect("share:dashboard")
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
            return redirect("share:dashboard")
        else:
            return render(request, "share/login.html", {"error":"Wrong username or password"})
    else:
        return redirect("share:dashboard")

#iserrano2
def logout_view(request):
    logout(request)
    return redirect("share:login")

#iserrano3
def dashboard(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login", {"user":user, "error":"Please Login"})
        else:
            # my_posts = Post.objects.filter(coder=user.coder.id)

            # return render(request, "share/dashboard.html",{"my_posts":my_posts})
            return render(request, "share/dashboard.html")

def user_profile(request, user_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login", {"user":user, "error":"Please Login"})
        else:
            user = get_object_or_404(User, pk=user_id)
            # my_posts = get_list_or_404(Post, user=user.id)

            my_posts = Post.objects.filter(user=user.id)
            my_profile = Profile.objects.get(user=user.id)
            print("my_profile: ", my_profile)

            # try:
            #     my_icon = Photo.objects.get(photo=my_profile.icon.photo)
            # except:
            # my_icon = Photo.getPhoto(my_profile.icon)
                # my_icon = os.stat("share/images/user_icon.png")
            # print("icon: ", my_icon)
            # my_icon = "media/"

            parameters = {
                "user":user,
                "my_posts":my_posts,
                "my_profile":my_profile
                # "my_icon":my_icon
            }
            return render(request, "share/user_profile.html", parameters)
            # return render(request, "share/user_profile.html", {"my_posts":my_posts, "my_icon":my_icon})

#iserrano4
def edit_profile(request, user_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login", {"user":user, "error":"Please Login"})

        #button is pressed, retrieve user information
        user_info = get_object_or_404(User, pk=user_id)
        my_profile = Profile.objects.get(user=user.id)


        #make sure the logged in user is the correct one
        if user_info.id == user.id:
            return render(request, "share/edit_profile.html", {"user_info":user_info, "my_profile":my_profile})
        else:
            return render(request, "share/login.html",
            {"Error": "Please login to edit profile"})


#iserrano6
# def update_profile(request, user_id):
#     if request.method == "POST":
#         user = request.user
#         if not user.is_authenticated:
#             return redirect("share:login", {"user":user, "error":"Please Login"})
#
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             return redirect('share/dashboard.html', {"user":user, "error":"Profile Settings Updated!"})
#
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#
#     context = {
#         'u_form':u_form,
#         'p_form':p_form
#     }
#
#     return render(request, 'share/dashboard.html', context)

#iserrano4
def update_profile(request, user_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)

        user_info = get_object_or_404(User, pk=user_id)
        user_profile = get_object_or_404(Profile, pk=user_id)

        if not request.POST.get('username') or not request.POST.get('email'):
            print("I am inside if")
            return render(request, "share/edit_profile.html", {"user_info":user_info, "Error":"Fill out required fields"})
        else:
            page_name = request.POST.get('page_name')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            icon = request.FILES.get("icon")
            # password = request.POST['password']
            
            # create Photo object
            photo = Photo.objects.create(user = user, photo = icon)


        if user_info.id == user.id:
            User.objects.filter(pk=user_id).update(first_name=first_name, last_name=last_name, username=username, email=email)
            print("I'm here")
            Profile.objects.filter(pk=user_id).update(page_name=page_name, icon=photo)
            photo.save()
            user=get_object_or_404(User, pk=user_id)
            user = request.user
            all_posts=Post.objects.all()
            return render(request, "share/user_profile.html", {"user":user, "all_posts":all_posts, "error":"Profile Updated!"})
        else:
            return render(request, "share/edit_profile.html", {"error":"Unable to update profile"})

    else:
        user = request.user
        all_posts=Post.objects.all()
        return render(request, "share/user_profile", {"user":user, "all_posts":all_posts, "error":"not a post request!"})



#iserrano4
def delete_profile(request, user_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login", {"user":user, "error":"Please Login"})

        user_info = get_object_or_404(User, pk=user_id)

        if user_info.id == user.id:
            User.objects.get(pk=user_id).delete()
            return redirect("share/signup.html")
        else:
            return render(request, "share/edit_profile.html", {"user":user, "error": "Unable to delete account"})


#iserrano4
def show_post(request, post_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login", {"user":user, "error":"Please Login"})
        else:
            post = get_object_or_404(Post, pk=post_id)

            # comments = Comment.objects.filter(post=post_id)
            # user_comment = Comment.objects.filter(user=user.id).filter(post=post.id)

        return render(request, "share/post.html", {"post":post})

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
            return render(request, "share/dashboard.html", {"error":"Created Post!"})


        except:
            return render(request, "share/publish_post_form.html", {"error":"Unable to publish post at this time"})

    else:
        user=request.user
        all_posts = Post.objects.all()
        return render(request, "share/dashboard.html", {"user":user, "error":"Unable to create a post at this time"})
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

        if not request.POST.get('post_header') and not request.POST.get('post_body'):
            return render(request, "share/edit_post.html", {"user":user, "post":post, "error":"Please fill in at least one field"})

        else:
            # photo = request.POST.get("photo")
            post_header = request.POST.get("post_header")
            post_body = request.POST.get("post_body")

            if post.user.id == user.id:
                # Photo.objects.filter(pk=post_id).update(photo=photo)
                Post.objects.filter(pk=post_id).update(post_header=post_header, post_body=post_body)
                post = get_object_or_404(Post, pk=post_id)
                all_posts=Post.objects.all()
                return render(request, "share/dashboard.html", {"user":user, "all_posts":all_posts, "error":"Post updated"})
            else:
                return render(request, "share/edit_post.html", {"error":"Unable to update post"})

    else:
        user = request.user
        all_posts = Post.objects.all()
        return render(request, "share/user_profile.html", {"user":user, "all_posts":all_posts, "error":"It was not a POST request"})

#iserrano4
def delete_post(request, post_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login", {"user":user, "error":"Please Login"})

        post = get_object_or_404(Post, pk=post_id)

        if post.user.id == user.id:
            Post.objects.get(pk=post_id).delete()
            return render(request, "share/dashboard.html", {"error":"Post Deleted!"})
        else:
            return render(request, "share/dashboard.html", {"error": "Non-authorized user; Unable to delete post"})

#iserrano4
def create_comment(request, post_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login", {"user":user, "error":"Please Login"})

        post = get_object_or_404(Post, pk=post_id)
        print("*************************Testing")
        print(post)
        commenter = user
        print("*************************Testing")
        print(commenter)
        comment_body = request.POST.get('comment_body')
        print("*************************Testing")
        print(comment_body)

        try:
            comment = Comment.objects.create(commenter=commenter, comment_body=comment_body)
            comment.save()

            comment = Comment.objects.filter(post=post_id)
            user_comment = Comment.objects.filter(commenter=user.id).filter(post=post.id)

            return render(request, "share/post.html", {"user":user, "post":post, "comments":comments, "user_comment":user_comment})

        except:
            return render(request, "share/post.html", {"error":"Unable to leave a comment at the moment!"})

    else:
        return render(request, "share/post.html", {"error":"Unable to load leave a comment!"})


def delete_comment(request, comment_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login", {"user":user, "error":"Please Login"})

        comment = get_object_or_404(Comment, pk=comment.id)
        post = get_object_or_404(Post, pk=comment.post.id)

        if comment.user.id == user.id:
            Comment.objects.get(pk=comment.id).delete()

            comment = Comment.objects.filter(post=post.id)
            user_comment = Comment.objects.filter(commenter=user.id).filter(post=post.id)
            return render(request, "share/post.html", {"user":user, "post":post, "comments":comments, "user_comment":user_comment})

        else:
            user_comment = Comment.objects.filter(commenter=user.id).filter(post=post.id)
            return render(request, "share/post.html", {"user":user, "post":post, "comments":comments, "user_comment":user_comment, "error":"Unable to delete comment at the moment!"})

    else:
        return HttpResponse(status=500)


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


#iserrano6
def search(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login", {"user":user, "error":"Please Login"})

        query = request.POST["query"]

        if not query:
            return render (request, "share/search_posts.html", {"error":"There's nothing here =("})

        posts = Post.objects.filter(post_header__icontains=query) | Post.objects.filter(post_body__icontains=query)

        return render(request, "share/search_posts.html", {"user":user, "posts":posts})

    else:
        return HttpResponse(status=500)
