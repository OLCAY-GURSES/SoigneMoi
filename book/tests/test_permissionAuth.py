from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from book.models import Patient, Doctor
User = get_user_model()

class PermissionsAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(

            email='admin@example.com',
            password='adminpass',
            is_staff=True,
            is_superuser=True
        )

        self.patient_user = User.objects.create_user(

            email='patient@example.com',
            password='patientpass',
            is_patient=True
        )

        self.doctor_user = User.objects.create_user(

            email='doctor@example.com',
            password='doctorpass',
            is_doctor=True
        )

        self.patient = Patient.objects.create(user=self.patient_user)
        self.doctor = Doctor.objects.create(user=self.doctor_user)

        self.login_url = reverse('login')
        self.patient_dashboard_url = reverse('patient-dashboard')
        self.admin_dashboard_url = reverse('admin-dashboard')

    def test_patient_login_and_dashboard_access(self):
        # Test login
        response = self.client.post(self.login_url, {
            'email': 'patient@example.com',
            'password': 'patientpass'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard
        self.assertRedirects(response, self.patient_dashboard_url)

        # Test access to patient dashboard
        self.client.login(email='patient@example.com', password='patientpass')
        response = self.client.get(self.patient_dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Patient Dashboard')

    def test_admin_login_and_dashboard_access(self):
        # Test login
        response = self.client.post(self.login_url, {
            'email': 'admin@example.com',
            'password': 'adminpass'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard
        self.assertRedirects(response, self.admin_dashboard_url)

        # Test access to admin dashboard
        self.client.login(email='admin@example.com', password='adminpass')
        response = self.client.get(self.admin_dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Dashboard')

    def test_doctor_login_and_dashboard_access(self):
        # Test login
        response = self.client.post(self.login_url, {
            'email': 'doctor@example.com',
            'password': 'doctorpass'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard
        self.assertRedirects(response, self.patient_dashboard_url)

        # Test access to patient dashboard
        self.client.login(email='doctor@example.com', password='doctorpass')
        response = self.client.get(self.patient_dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Patient Dashboard')

    def test_unauthenticated_user_redirect(self):
        response = self.client.get(self.patient_dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.patient_dashboard_url}')

        response = self.client.get(self.admin_dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.admin_dashboard_url}')