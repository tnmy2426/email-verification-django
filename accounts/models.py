from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    #adding new field in User model
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='profilepic.jpg',upload_to='profile_pictures')
    #location=models.CharField(max_length=100)
    First_Name=models.CharField(default='John',max_length=20)
    Last_Name=models.CharField(default='Doe',max_length=30)

    def __str__(self):
        return self.user.username


class LoggedInUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='logged_in_user')
    session_key=models.CharField(max_length=32,null=True,blank=True)
    

    def __str__(self):
        return self.user.username