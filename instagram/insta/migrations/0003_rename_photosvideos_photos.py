# Generated by Django 5.0.6 on 2024-06-07 01:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0002_rename_firstname_fbsignup_fullname'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='photosvideos',
            new_name='photos',
        ),
    ]
