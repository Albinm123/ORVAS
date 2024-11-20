from django import forms
from .models import *


class MecRequestForm(forms.ModelForm):
    
    class Meta:
        model=ServiceRequest
        fields=('location','phone','issue','issue_description')
        
class RequestFeedbackForm(forms.ModelForm):
    class Meta:
        model=ServiceFeedback
        fields=('total_bill','rating','comments')