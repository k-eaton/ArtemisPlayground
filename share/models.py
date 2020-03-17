from django.db import models

# Create your models here.
# iserrano0 - Script model
class Script(models.Model):
	title = models.CharField(max_length=30, null=False, blank=False, unique=False)
	description = models.TextField(max_length=100, null=False, blank=False, unique=False)
	# user can enter a a piece of code or an url
	code = models.TextField(max_length=10000, unique=False)
	url = models.URLField(unique=False, blank=True)

	def __str__(self):
		return self.title
