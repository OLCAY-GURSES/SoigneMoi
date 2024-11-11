from django.test import TestCase
from book.forms import CustomUserCreationForm, PatientForm, DoctorForm, SecretaryForm, EditDoctorForm, EditSecretaryForm
from book.models import User, Patient, Hospital, Specialization, Doctor, Secretary

class FormsTestCase(TestCase):

    def setUp(self):
        self.hospital = Hospital.objects.create(name='Test Hospital')
        self.specialization = Specialization.objects.create(hospital=self.hospital, specialization_name='Cardiology')
        self.user = User.objects.create_user(email='test@example.com', password='password123')

    def test_custom_user_creation_form(self):
        form_data = {'email': 'newuser@example.com', 'password1': 'ComplexPassword123!', 'password2': 'ComplexPassword123!'}
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_patient_form(self):
        form_data = {'first_name': 'John', 'last_name': 'Doe', 'phone_number': '1234567890', 'date_of_birth': '2000-01-01', 'address': '123 Street'}
        form = PatientForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_doctor_form(self):
        form_data = {
            'first_name': 'John', 'last_name': 'Doe', 'phone_number': '1234567890',
            'date_of_birth': '2000-01-01', 'hospital_name': self.hospital.pk, 'specialization': self.specialization.pk,
            'email': 'doctor@example.com', 'password1': 'ComplexPassword123!', 'password2': 'ComplexPassword123!'
        }
        form = DoctorForm(data=form_data)
        form.fields['specialization'].queryset = Specialization.objects.filter(hospital_id=self.hospital.pk)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_secretary_form(self):
        form_data = {
            'first_name': 'Jane', 'last_name': 'Doe', 'phone_number': '0987654321', 'date_of_birth': '1990-01-01',
            'address': '456 Avenue', 'hospital_name': self.hospital.pk, 'email': 'secretary@example.com',
            'password1': 'ComplexPassword123!', 'password2': 'ComplexPassword123!'
        }
        form = SecretaryForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_edit_doctor_form(self):
        doctor = Doctor.objects.create(user=self.user, first_name='John', last_name='Doe', specialization=self.specialization, hospital_name=self.hospital)
        form_data = {
            'first_name': 'John', 'last_name': 'Doe', 'phone_number': '1234567890', 'date_of_birth': '2000-01-01',
            'hospital_name': self.hospital.pk, 'specialization': self.specialization.pk, 'reg_number': '12345', 'email': 'doctor@example.com'
        }
        form = EditDoctorForm(instance=doctor, data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_edit_secretary_form(self):
        secretary = Secretary.objects.create(user=self.user, first_name='Jane', last_name='Doe', hospital_name=self.hospital)
        form_data = {
            'first_name': 'Jane', 'last_name': 'Doe', 'phone_number': '0987654321', 'date_of_birth': '1990-01-01',
            'hospital_name': self.hospital.pk, 'reg_number': '54321', 'email': 'secretary@example.com'
        }
        form = EditSecretaryForm(instance=secretary, data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)