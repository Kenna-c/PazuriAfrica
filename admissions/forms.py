from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'program', 'id_copy', 'certificate']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'id_copy': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'certificate': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
