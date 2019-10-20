from django import forms
from .models import list

class listForm(forms.ModelForm):
    class Meta:
        model = list
        fields = ["item", "completed"]
