from django.contrib import admin

# Register your models here.
#iserrano1
from .models import Coder, Problem, Script, Photo

admin.site.register(Script)
admin.site.register(Problem)
admin.site.register(Coder)
admin.site.register(Photo)
