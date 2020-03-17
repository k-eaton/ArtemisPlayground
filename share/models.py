from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
