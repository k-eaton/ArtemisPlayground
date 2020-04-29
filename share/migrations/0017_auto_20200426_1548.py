# Generated by Django 3.0.4 on 2020-04-26 22:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('share', '0016_auto_20200426_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='icon',
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together={('user', 'post')},
        ),
    ]