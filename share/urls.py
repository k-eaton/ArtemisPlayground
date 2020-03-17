from django.urls import path, include
from . import views  #import everything from views module

#iserrano0
app_name = 'share'
urlpatterns = [
    path('',views.index, name='index'),
]
