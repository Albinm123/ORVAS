from django.db import models
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
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)  
    car_img=models.ImageField(null=True,upload_to="media\car_img")


class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)  
    rental_start_date = models.DateTimeField(default=timezone.now)
    rental_end_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_completed = models.BooleanField(default=False)

class RentalFeedback(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
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