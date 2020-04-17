from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.fields import DateTimeField
#attempt hashtags later:
#https://stream-blog.netlify.app/build-a-scalable-twitter-clone-with-django-and-stream/#hashtags-feeds
# from django.template.defaultfilters import slugify


# Create your models here.
#iserrano1 - create Coder model
class Coder(models.Model):
    def __str__(self):
        return self.user.username

    coder_yet = models.BooleanField(default=False)  # the user is not a coder yet
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now=True)   # maybe redundant, user model has date_joined
    updated = models.DateField(auto_now=True)

#iserrano1 - Create Problem model
class Problem(models.Model):
    def __str__(self):
        return self.title
    coder = models.ForeignKey(Coder, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False, unique=False)
    description = models.TextField(max_length=100, null=False, blank=False, unique=False)
    image = models.ImageField(upload_to='myproblems/', blank=True)
    discipline = models.CharField(max_length=50, null=False, blank=False, unique=False)
    make_public = models.BooleanField(default=True)
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now=True)     # everytime the obj is saved, new time is saved

#iserrano1 - update Script model
class Script(models.Model):
    def __str__(self):
        return self.title
    # FK
    coder = models.ForeignKey(Coder, on_delete=models.CASCADE, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=50, null=False, blank=False, unique=False)
    description = models.TextField(max_length=100, null=False, blank=False, unique=False)
    code = models.TextField(max_length=10000, unique=False)
    url = models.URLField(max_length=300, unique=False, blank=True)

    input = models.TextField(max_length=100, unique=False, blank=True)
    output = models.TextField(max_length=100, unique=False, blank=True)
    make_public = models.BooleanField(default=True)

    image = models.ImageField(upload_to='myscripts/', blank=True)  # add an image for the algorithm or flow chart
    working_code = models.BooleanField(default=True)

    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now=True)

#iserrano4 - create Media Model
#REMEMBER TO DO THEM ONE AT A TIME
class Media(models.Model):
    def __str__(self):
        return self.title

    #FK
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    file_name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    video = models.BooleanField(default=False)
    thumb_nail = models.ImageField(default="default.png", blank=True)

#iserrano4 - create Post Model
#REMEMBER TO DO THEM ONE AT A TIME
class Post(models.Model):
    def __str__(self):
        return self.title

    #FK
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE, blank=True, null=True)

    post_header = models.CharField(max_length=50, blank=True, unique=False)
    post_body = models.TextField(max_length=500, blank=True, unique=False)
    post_created = DateTimeField(auto_now_add=True)
    post_updated = DateTimeField(auto_now=True)

    # #attemping to incorporate parse_hastags
    # tags = []
    # for hastag in self.parse_hastags():
    #     tags.append(feed_manager.get_feed('hastag', hastag))
    # return tags

#iserrano4 - create Comment Model
#REMEMBER TO DO THEM ONE AT A TIME
class Comment(models.Model):
    def __str__(self):
        return self.title

    #FK
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    comment_created = DateTimeField(auto_now_add=True)
    comment_updated = DateTimeField(auto_now=True)
    comment_body = models.TextField(max_length=200, unique=False, blank=False)


#iserrano4 - attempt to create Hastag Model
#REMEMBER TO DO THEM ONE AT A TIME
# class Hastag(models.Model):
#     def__str__(self):
#         return self.title
#
#     hastag = models.CharField(max_length=100, blank=False, unique=True)
