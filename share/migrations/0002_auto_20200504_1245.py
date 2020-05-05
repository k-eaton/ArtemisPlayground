# Generated by Django 3.0.3 on 2020-05-04 12:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('share', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='users',
            field=models.ManyToManyField(related_name='friend', to=settings.AUTH_USER_MODEL),
        ),
    ]
