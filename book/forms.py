from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Patient


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User

        fields = ['email', 'password1', 'password2']



    # create a style for model form
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control floating'})


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['last_name','first_name', 'phone_number', 'date_of_bird','address']

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class PasswordResetForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']

    # create a style for model form
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control floating'})