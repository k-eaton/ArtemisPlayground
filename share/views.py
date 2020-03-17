from django.shortcuts import render
from django.http import HttpResponse
from share.models import Script

# Create your views here.
#iserrano0
def index(request):
    if request.method == "GET":
        return HttpResponse("Hello World!")
