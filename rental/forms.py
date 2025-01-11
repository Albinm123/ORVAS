from django import forms
from .models import RentalFeedback,Car


class RentalFeedbackForm(forms.ModelForm):
    class Meta:
        model=RentalFeedback
        fields=('rating','comment')
        
class AddCarForm(forms.ModelForm):
    class Meta:
        model=Car
        exclude =('is_active','created_at')
        

class UpdateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            "make", "model", "year", "car_type", "color", "registration_number",
            "is_available", "price_per_hour", "price_per_day", "price_for_week",
            "mileage_per_liter", "car_img", "car_discription", "is_active"
        ]