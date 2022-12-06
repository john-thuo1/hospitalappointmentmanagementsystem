from tabnanny import verbose
# from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import User
from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

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

# The relationship here is 1-1 since only one user can be associated with 1 profile
# Once the user is deleted, the profile is also deleted hence on_delete = models.CASCADE

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image= models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

# The method is used to resive the profile photos uploaded by users
# It uses the save() method from parent class and reuses the method to save image once it has been resized
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 350 or img.width > 350:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)