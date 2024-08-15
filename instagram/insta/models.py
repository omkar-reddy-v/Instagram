from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class instasignup(models.Model):
    mobile = models.BigIntegerField()
    fullname = models.CharField( max_length=50)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='instagram/')



    def __str__(self):
        return f"{self.mobile} {self.fullname} {self.uid}"
    

class photos(models.Model):
    photoid = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='instagram/')


class Videos(models.Model):
    videoid = models.ForeignKey(User,on_delete=models.CASCADE)
    video = models.FileField(upload_to='instagram/', blank=True, null=True)



# this Models for facebook

class Fbsignup(models.Model):
    firstname = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=50)
    fbuid = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='instagram/')



    def __str__(self):
        return f"{self.firstname} {self.surname} {self.dob} {self.gender}"