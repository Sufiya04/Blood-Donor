from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

class DonorForm(forms.ModelForm):
    class Meta:
        model=Donor
        fields="__all__"

        widgets= {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'id': 'age'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood': forms.Select(attrs={'class': 'form-control'}),
            'smoker':forms.Select(attrs={'class': 'form-control', 'id': 'smoker'}),
            'alcoholic': forms.Select(attrs={'class': 'form-control', 'id': 'alcoholic'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact', 'id': 'contact'}),
            'units': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Units'}),
            'health': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Health Information'}),
            'last': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Last Donation Date'})
        }

class RecipientForm(forms.ModelForm):
    class Meta:
        model=Recipient
        fields="__all__"

        widgets= {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patient Name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood': forms.Select(attrs={'class': 'form-control'}),
            'units': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Units Required'}),
            'urgent': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Required Date'}),
            'hos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hospital Name'}),
            'add': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hospital Address'}),
            'requester': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Requester Name'})
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username= forms.EmailField(widget= forms.EmailInput())
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label="Enter your registered email")


class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(), label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        
        return cleaned_data
