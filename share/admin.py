from django.contrib import admin

# Register your models here.

from .models import Coder, Problem, Script, Media, Post, Comment, Photo, Profile, Friend, Follower


admin.site.register(Problem)
admin.site.register(Coder)
admin.site.register(Photo)
#iserrano4
admin.site.register(Media)
admin.site.register(Post)
admin.site.register(Comment)
#iserrano6
admin.site.register(Profile)
#iserrano7
admin.site.register(Friend)
admin.site.register(Follower)
