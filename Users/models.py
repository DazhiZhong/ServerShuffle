from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from .ImageMod import resize_and_crop



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to='profile_pics')
    bio = models.TextField(null=True,blank=False)

    def __str__(self):
        return f"{self.user.username} profile"
    
    # def save(self,*args, **kwargs):
    #     print('old -',self.image.path)
    #     super().save(*args, **kwargs)
    #     print('new -',self.image.path)
    #     resize_and_crop(self.image.path,self.image.path,(300,300),crop_type="middle")

    
