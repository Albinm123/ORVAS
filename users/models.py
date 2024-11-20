from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from location.models import Location
# Create your models here.
from django.contrib.auth import get_user_model


class CustomeUser(AbstractUser):
    USER_TYPES=(
        ('user','user'),
        ('mechanic','mechanic'),
        ('administrator','admin'),
    )
    user_type=models.CharField(max_length=200,choices=USER_TYPES)
    
            
class UserProfile(models.Model):
    user=models.OneToOneField(CustomeUser,on_delete=models.CASCADE,related_name='user_profile')
    addres=models.CharField(max_length=200)
    location=models.OneToOneField(Location,on_delete=models.CASCADE,related_name='user_location' ,null=True, blank=True)
    phone=models.CharField(max_length=200)
    dob=models.DateTimeField(null=True)
    bio=models.CharField(max_length=200)
    profile_pic=models.ImageField(null=True,upload_to='media/user_profile_img')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username
    

    
class MechanicProfile(models.Model):
    user=models.OneToOneField(CustomeUser,on_delete=models.CASCADE,related_name='mechanic_profile')
    addres=models.CharField(max_length=200)
    location=models.OneToOneField(Location,on_delete=models.CASCADE,related_name='mechanic_location',null=True, blank=True)
    phone=models.CharField(max_length=200)
    dob=models.DateTimeField(null=True)
    bio=models.CharField(max_length=200)
    skils=models.CharField(max_length=200)
    experience=models.IntegerField(default=0)
    is_approved=models.BooleanField(default=False)
    options=(
        ('two_wheeler','two_wheeler'),
        ('four_wheeler','four_wheeler'),
        ('heavy-vhehicle','heavy_vhehicle')
    )
    specialized_in=models.CharField(max_length=200,choices=options)
    available=models.BooleanField(default=True,)
    average_rating = models.FloatField(default=0.0)
    profile_pic=models.ImageField(null=True,upload_to='media/mechanic_profile_img')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.user.username
    
    def update_average_rating(self):
        feedbacks = self.user.feedbacks_received.all()
        total_rating = sum(feedback.rating for feedback in feedbacks)
        count = feedbacks.count()
        self.average_rating = total_rating / count if count > 0 else 0
        self.save()
   

def create_profile(sender,instance,created,**kwargs):
    if created and instance.user_type == 'user':
        UserProfile.objects.create(user=instance)
        
    if created and instance.user_type == 'mechanic':
        MechanicProfile.objects.create(user=instance)
        
post_save.connect(create_profile,sender=CustomeUser)

