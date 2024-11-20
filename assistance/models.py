from django.db import models
from users.models import CustomeUser,MechanicProfile
from location.models import Location
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
        ('accepted','Accept'),
    ]
    
    user=models.ForeignKey(CustomeUser,on_delete=models.CASCADE,related_name='user_request')
    mechanic=models.ForeignKey(CustomeUser,on_delete=models.CASCADE,related_name='assined_mechanic',
            limit_choices_to={'user_type':'mechanic'},null=True
            )
    location=models.ForeignKey(Location,on_delete=models.CASCADE,related_name='request_location')
    phone=models.IntegerField()
    request_time=models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    issue=models.CharField(max_length=200,null=True)
    issue_description = models.TextField()
    is_active=models.BooleanField(default=True)
    
    
    
class ServiceFeedback(models.Model):
    OPTIONS = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )
    
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    mechanic = models.ForeignKey(CustomeUser,
        on_delete=models.CASCADE, null=True, blank=True,
        related_name='feedbacks_received', limit_choices_to={'user_type': 'mechanic'}
    )
    
    total_bill=models.IntegerField()
    rating = models.IntegerField(choices=OPTIONS, default=5)
    comments = models.TextField(blank=True)  
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)


    
    # def issue(self):
    #     # Retrieve the issue from the related ServiceRequest
    #     return self.service_request.issue
    
@receiver(post_save, sender=ServiceFeedback)
def update_mechanic_rating(sender, instance, **kwargs):
    if instance.mechanic:
        instance.mechanic.mechanic_profile.update_average_rating()
        
