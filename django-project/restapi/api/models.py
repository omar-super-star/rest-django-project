from django.db import models

# Create your models here.
class users(models.Model):
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    firstname=models.CharField(max_length=125)
    lastname = models.CharField(max_length=125)
    favorite=models.CharField(max_length=500,null=True)