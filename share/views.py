from django.shortcuts import render, redirect #iserrano2
from django.http import HttpResponse
from share.models import Script
#iserrano2 - authentication, login, logout
from django.contrib.auth import authenticate, login, logout
#iserrano2 - import all models created
from .models import Script, Problem, Coder
#iserrano2 - import User model
from django.contrib.auth.models import User
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
            all_problems = Problem.objects.all()   # all_problems is a list object [   ]

            return render(request, "share/index.html", {"user":user, "all_problems": all_problems})
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
        coder_yet = request.POST.get('coder_yet_checkbox')

        if username is not None and email is not None and password is not None: # checking that they are not None
            if not username or not email or not password: # checking that they are not empty
                return render(request, "share/signup.html", {"error": "Please fill in all required fields"})
            if User.objects.filter(username=username).exists():
                return render(request, "share/signup.html", {"error": "Username already exists"})
            elif User.objects.filter(email=email).exists():
                return render(request, "share/signup.html", {"error": "Email already exists"})
            # save our new user in the User model
            user = User.objects.create_user(username, email, password)
            coder = Coder.objects.create(user= user, coder_yet = coder_yet).save()
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

#iserrano2
def publish_problem(request):
    pass

#iserrano3
def show_my_problem(request, problem_id):
    pass

#iserrano3
def show_my_script(request, script_id):
    pass

#iserrano3
def show_problem(request, problem_id):
    pass

#iserrano3
def show_script(request, script_id):
    pass

# s3Integration
def upload(request):
    if request.method == "POST" and request.FILES['myphoto']:
        title = request.POST['title']
        myphoto = request.FILES['myphoto']
        user = request.user

        # organize a path for the file in bucket
        file_directory_within_bucket = 'user_upload_files/user_{user_id}'.format(user_id=request.user.id)

        # synthesize a full file path; note that we included the filename
        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            myphoto.name
        )

        #save file to DB
        photo = Photo.objects.create(user = user, title = title, photo = myphoto) #.save()

        # save file to AWS
        media_storage = MediaStorage()
        # filename = media_storage.save(file_path_within_bucket, myphoto)



        uploaded_file_url = photo.photo
        photo.save()

        # uploaded_file_url = media_storage.url(filename)
        return render(request, 'share/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })

    return render(request, 'share/upload.html')
