from tabnanny import verbose
# from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Doctors(User):
    # Will have an additional phone_number field
    # Doctor_level = models.CharField(Required)
    phone_number = models.CharField(unique=True, max_length=17) 

    class Meta: 
        verbose_name_plural = 'Doctors'

class Patients(User):

    phone_number = models.CharField(unique=True, max_length=17)
    class Meta:
        verbose_name_plural = 'Patients'
