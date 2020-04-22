from django.contrib import admin

# Register your models here.
#iserrano1
<<<<<<< HEAD
from .models import Coder, Problem, Script, Photo
=======
from .models import Coder, Problem, Script, Media, Post, Comment
>>>>>>> ecaa37efc9e68ea87332cd2b2fe3d91168ddf2d4

admin.site.register(Script)
admin.site.register(Problem)
admin.site.register(Coder)
<<<<<<< HEAD
admin.site.register(Photo)
=======
#iserrano4
admin.site.register(Media)
admin.site.register(Post)
admin.site.register(Comment)
>>>>>>> ecaa37efc9e68ea87332cd2b2fe3d91168ddf2d4
