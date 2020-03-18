from django.urls import path, include
from . import views  #import everything from views module

#iserrano0
app_name = 'share'
urlpatterns = [
    path('',views.index, name='index'),
    #iserrano2
    # authentication: signup, login, logout
    path('create', views.create, name='create'),
    path("loguser", views.login_user, name="loguser"),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.signup, name='signup'),
    #iserrano2
    #dashboard & publish_problem
    path("dashboard", views.dashboard, name='dashboard'),
    path('publish_problem', views.publish_problem, name='publish_problem'),

]
