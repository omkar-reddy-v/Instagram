# Generated by Django 5.0.6 on 2024-07-02 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0004_videos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fbsignup',
            old_name='fullname',
            new_name='firstname',
        ),
    ]