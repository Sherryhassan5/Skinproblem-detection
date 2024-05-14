from django import forms
from .models import CapturedImage

class ImageForm(forms.ModelForm):
    class Meta:
        model = CapturedImage
        fields = ['image']