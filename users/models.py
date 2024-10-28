from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from location.models import Location
# Create your models here.

class CustomeUser(AbstractUser):
    USER_TYPES=(
        ('admin','admin'),
        ('user','user'),
        ('mechanic','mechanic'),
    )
    user_type=models.CharField(max_length=200,choices=USER_TYPES)
    
    
class UserProfile(models.Model):
    user=models.OneToOneField(CustomeUser,on_delete=models.CASCADE,related_name='user_profile')
    addres=models.CharField(max_length=200)
    location=models.OneToOneField(Location,on_delete=models.CASCADE,related_name='user_location')
    phone=models.CharField(max_length=200)
    dob=models.DateTimeField(null=True)
    bio=models.CharField(max_length=200)
    profile_pic=models.ImageField(null=True,upload_to='media/user_profile_img')
    
    
    def __str__(self):
        return self.user.username
    

    
class MechanicProfile(models.Model):
    user=models.OneToOneField(CustomeUser,on_delete=models.CASCADE,related_name='mechanic_profile')
    addres=models.CharField(max_length=200)
    location=models.OneToOneField(Location,on_delete=models.CASCADE,related_name='mechanic_location')
    phone=models.CharField(max_length=200)
    dob=models.DateTimeField(null=True)
    bio=models.CharField(max_length=200)
    skils=models.CharField(max_length=200)
    experience=models.IntegerField()
    is_approved=models.BooleanField(default=False)
    options=(
        ('two_wheeler','two_wheeler'),
        ('four_wheeler','four_wheeler'),
        ('heavy-vhehicle','heavy_vhehicle')
    )
    specialized_in=models.CharField(max_length=200,choices=options)
    available=models.BooleanField(default=True,)
    profile_pic=models.ImageField(null=True,upload_to='media/mechanic_profile_img')
    
    
    def __str__(self):
        return self.user.username
   
   

def create_profile(sender,instance,created,**kwargs):
    if created and instance.user_type == 'user':
        UserProfile.objects.create(user=instance)
        
    if created and instance.user_type == 'mechanic':
        MechanicProfile.objects.create(user=instance)
        
post_save.connect(create_profile,sender=CustomeUser)