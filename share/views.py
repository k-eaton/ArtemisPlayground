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
#iserrano4 - import new models created
#REMEMBER TO DO THEM ONE AT A TIME
# from .models import Media, Post, Comment

# Create your views here.
#iserrano2
def signup(request):
    if request.user.is_authenticated:
        return redirect("share:index")
    return render(request, 'share/signup.html')

#iserrano2
def create(request):
    if request.method == "POST":
        username = request.POST['Username']
        email = request.POST['Email']
        password = request.POST['Password']
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

#iserrano4
def edit_profile(request, user_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")

        #button is pressed, retrieve user information
        user_info = get_object_or_404(User, pk=user.id)

        #make sure the logged in user is the correct one
        if user_info.id == user.id:
            return render(request, "share/edit_profile.html", {"user_info":user_info})
        else:
            return render(request, "share/index.html",
            {"Error": "Please login to edit profile"})


def update_profile(request):
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

def delete_profile(request):
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


#useless code
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
