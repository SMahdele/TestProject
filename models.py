from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE )
    phone= models.IntegerField()
    dob= models.CharField(max_length=100)
    profile_pic=models.ImageField(upload_to='uploads/profile_pics/',blank=True)

    def __str__(self):
        return self.user.username

class Book(models.Model):
    author= models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=256)
    lunch_date=models.DateTimeField()
    price=models.FloatField()

    def __str__(self):
        return self.name
