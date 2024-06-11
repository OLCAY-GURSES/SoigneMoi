from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import User, Patient, Hospital, Specialization, Doctor, Secretary, DoctorTimeSlots


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
        fields = ['last_name','first_name', 'phone_number', 'date_of_birth','address']

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


class AddHospitalForm(ModelForm):
    class Meta:
        model = Hospital
        fields = ['name','address','featured_image','phone_number','email','description']

    def __init__(self, *args, **kwargs):
        super(AddHospitalForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class EditHospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['name','address','featured_image','phone_number','email','description']

    def __init__(self, *args, **kwargs):
        super(EditHospitalForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})



class DoctorForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmer le mot de passe')

    specialization = forms.ModelChoiceField(queryset=Specialization.objects.none(), required=True,
                                            label='Spécialisation')
    hospital_name = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True, label='Hôpital')

    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Date de naissance')

    class Meta:
        model = Doctor
        fields = ['last_name','first_name', 'date_of_birth', 'phone_number', 'hospital_name', 'specialization']
        labels = {
            'last_name': 'Nom',
            'first_name': 'Prénom',
            'date_of_birth': 'Date de naissance',
            'phone_number': 'Numéro de téléphone',
        }

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        # Check if data is being posted
        if 'hospital_name' in self.data:
            try:
                hospital_id = int(self.data.get('hospital_name'))
                self.fields['specialization'].queryset = Specialization.objects.filter(hospital_id=hospital_id)
            except (ValueError, TypeError):
                self.fields['specialization'].queryset = Specialization.objects.none()
        elif self.instance.pk:
            hospital_id = self.instance.hospital_name.hospital_id
            self.fields['specialization'].queryset = Specialization.objects.filter(hospital_id=hospital_id)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les deux mots de passe ne correspondent pas.")
        return password2

class EditDoctorForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    #date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Date de naissance')

    class Meta:
        model = Doctor
        fields = ['last_name', 'first_name', 'phone_number', 'date_of_birth', 'hospital_name', 'specialization', 'reg_number', 'email']
        labels = {
            'last_name': 'Nom',
            'first_name': 'Prénom',
            'date_of_birth': 'Date de naissance',
            'phone_number': 'Numéro de téléphone',
            'hospital_name': 'Hôpital',
            'specialization': 'Spécialisation',
            'reg_number': 'Matricule',
        }

    def __init__(self, *args, **kwargs):
        super(EditDoctorForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.user:
            self.fields['email'].initial = instance.user.email

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorTimeSlots
        fields = ['doc_start_date', 'doc_end_date']
        labels = {
            'doc_start_date': 'Début',
            'doc_end_date': 'Fin',

        }
        widgets = {
            'doc_start_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'id_doc_start_date'}),
            'doc_end_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'id_doc_end_date'}),
        }

class DoctorTimeSlotForm(forms.ModelForm):
    class Meta:
        model = DoctorTimeSlots

        fields = ['doctor','doc_start_date', 'doc_end_date']

class SecretaryForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmer le mot de passe')
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Date de naissance')

    hospital_name = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True, label='Hôpital')

    class Meta:
        model = Secretary
        fields = ['last_name','first_name', 'date_of_birth', 'phone_number', 'address', 'hospital_name']
        labels = {

            'last_name': 'Nom',
            'first_name': 'Prénom',
            'date_of_birth': 'Date de naissance',
            'phone_number': 'Numéro de téléphone',
            'address': 'Adresse',
            'hospital_name': 'Hôpital',
        }

    def __init__(self, *args, **kwargs):
        super(SecretaryForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les deux mots de passe ne correspondent pas.")
        return password2

class EditSecretaryForm(forms.ModelForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = Secretary
        fields = ['first_name', 'last_name', 'phone_number', 'date_of_birth', 'hospital_name', 'reg_number', 'email']
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'date_of_birth': 'Date de naissance',
            'phone_number': 'Numéro de téléphone',
            'hospital_name': 'Hôpital',
            'reg_number': 'Matricule',
        }

    def __init__(self, *args, **kwargs):
        super(EditSecretaryForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.user:
            self.fields['email'].initial = instance.user.email

        for name, field in self.fields.items():
            if name == 'date_of_birth':
                field.widget.attrs.update({'class': 'form-control', 'type': 'date'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
