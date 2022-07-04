from tabnanny import verbose
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# from django.core.validators import RegexValidator



# Create your models here.
class Doctors(User):
    
    phone_number = models.CharField(unique=True, max_length=17)
    
    class Meta:
        verbose_name_plural = 'Doctors'



class Patients(User):

    phone_number = models.CharField(unique=True, max_length=17)
    class Meta:
        verbose_name_plural = 'Patients'
