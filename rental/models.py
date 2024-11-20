from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomeUser
from django.utils import timezone
# Create your models here.

class Car(models.Model):
    CAR_TYPES = (
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('hatchback', 'Hatchback'),
        ('truck', 'Truck'),
    )
    
    make = models.CharField(max_length=100)  
    model = models.CharField(max_length=100)  
    year = models.PositiveIntegerField()  
    car_type = models.CharField(max_length=20, choices=CAR_TYPES)
    color = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=50, unique=True)  
    is_available = models.BooleanField(default=True)  
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)  
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2) 
    price_for_week = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)  
    mileage_per_liter = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    car_img=models.ImageField(null=True,upload_to="media\car_img")
    car_discription=models.CharField(max_length=200,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.make} {self.model}"
    
    def update_rent(self):
        self.price_for_week=(self.price_per_day*7)
        self.price_per_hour=(self.price_per_day/24)
        self.save(update_fields=['price_for_week','price_per_hour'])
        
    
class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE,related_name="rental_car")
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)  
    rental_start_date = models.DateTimeField(default=timezone.now)
    rental_end_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    
class RentalFeedback(models.Model):
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE,related_name="rental_feedback")
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[
        (1, "1 - Poor"),
        (2, "2 - Fair"),
        (3, "3 - Good"),
        (4, "4 - Very Good"),
        (5, "5 - Excellent"),
    ])
    comment = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    
    
@receiver(post_save, sender=Car)
def update_rent_on_save(sender, instance, **kwargs):
    if not kwargs.get('update_fields') or 'price_for_week' not in kwargs['update_fields']:
        instance.update_rent()