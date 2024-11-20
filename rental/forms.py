from django import forms
from .models import RentalFeedback,Car


class RentalFeedbackForm(forms.ModelForm):
    class Meta:
        model=RentalFeedback
        fields=('rating','comment')
        
class AddCarForm(forms.ModelForm):
    class Meta:
        model=Car
        fields='__all__'