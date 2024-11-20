from django.db import models

# Create your models here.
class Location(models.Model):
    loc_name=models.CharField(max_length=200)
    loc_discription=models.CharField(max_length=100,null=True,blank=True)
    lattitude=models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)
    longitude=models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.loc_name
    
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"