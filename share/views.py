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
def show_media(request):
    s3 = boto3.resource('s3',region_name='us-east-2')
    bucket = s3.Bucket('artemisplayground')
    object = bucket.Object('diablo.jpg')
    object.download_file('diablo.jpg')
    # with open('FILE_NAME', 'wb') as f:
    #     s3.download_fileobj('artemisplayground', 'diablo.jpg', f)
    # f = s3.download_file('artemisplayground', 'diablo.jpg', 'diablo.jpg')
    # for bucket in s3.buckets.all():
    #     print(bucket.name)
    # s3.download_file('artemisplayground', 'diablo.jpg', 'diablo.jpg')
    return diablo.jpg