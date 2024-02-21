import os
from datetime import datetime, date, timedelta

import django

# Configurer les paramètres Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgm_system.settings')
django.setup()
AUTH_USER_MODEL = 'book.User'

import unittest
from django.contrib.auth import get_user_model, authenticate
from book.models import *
from datetime import date

from book.views import get_unavailable_dates

from django.contrib.auth import get_user_model
from book.models import Patient
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, AbstractUser
from book.models import Doctor, Appointment

User = get_user_model()


class PatientRegisterTestCase(TestCase):
    def setUp(self):
        self.register_url = '/patient-register/'
        self.user_data = {
            'email': 'patient10@gmail.com',
            'password': 'testpassword'
        }

    def test_create(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 200)  # Redirect status code

        # Vérifier si l'utilisateur a été créé et est marqué comme patient
        self.user = User.objects.create(email=self.user_data['email'], password=self.user_data['password'])


    def test_str(self):
        user = User.objects.create(email='patient10@gmail.com', password='testpassword')
        self.assertEqual(str(user), user.email)


class PatientDashboardTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='patient10@gmail.com', password='testpassword')
        self.patient = Patient.objects.create(user=self.user)
        self.doctor = Doctor.objects.create(user=User.objects.create_user(email='doctor@example.com',
                                                                          password='testpassword'))
        self.appointment = Appointment.objects.create(patient=self.patient, doctor=self.doctor,
                                                      start_date='2024-02-20')
        self.prescription = Prescription.objects.create(patient=self.patient)

    def test_patient_dashboard_authenticated(self):
        self.client.login(email='patient10@gmail.com', password='testpassword')
        response = self.client.get(reverse('patient-dashboard'))
        self.assertEqual(response.status_code, 302)  # OK status code

    def test_patient_dashboard_unauthenticated(self):
        response = self.client.get(reverse('patient-dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_patient_dashboard_non_patient(self):
        self.user.is_patient = False
        self.user.save()
        self.client.login(email='patient10@gmail.com', password='testpassword')
        response = self.client.get(reverse('patient-dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to logout


class ProfileSettingsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='patient10@gmail.com', password='testpassword')
        self.profile_settings_url = reverse('profile-settings')

        self.form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '01-01-1990',
            'phone_number': '1234567890',
            'address': '123 Main St'
        }

    def test_profile_settings_authenticated_patient(self):
        self.client.login(email='patient10@gmail.com', password='testpassword')
        response = self.client.post(self.profile_settings_url, self.form_data)
        self.assertEqual(response.status_code, 302)  # Redirection status code

    def test_profile_settings_unauthenticated_redirect_to_login(self):
        response = self.client.get(self.profile_settings_url)
        self.assertEqual(response.status_code, 302)  # Redirection to login page

    def test_profile_settings_non_patient_redirect_to_logout(self):
        non_patient_user = User.objects.create_user(email='patient12@gmail.com', password='testpassword')
        self.client.force_login(non_patient_user)

        response = self.client.get(self.profile_settings_url)
        self.assertEqual(response.status_code, 302)  # Redirection to logout page

        response = self.client.post(self.profile_settings_url)
        self.assertEqual(response.status_code, 302)  # Redirection to logout page




class BookingTestCase(TestCase):
    def setUp(self):
        # Créer un utilisateur patient
        self.patient_user = User.objects.create_user(email='patient1@example.com', password='password')
        self.patient = Patient.objects.create(user=self.patient_user)

        # Créer un médecin
        self.doctor = Doctor.objects.create(last_name='Dr. John Doe')

    def test_available_booking(self):
        # Se connecter en tant que patient
        self.client.login(email='patient1@example.com', password='password')

        # Définir les données du formulaire pour la réservation
        form_data = {
            'appoint_start_date': '2024-03-01',
            'appoint_end_date': '2024-01-14',
            'message': 'Test de rendez-vous',
        }

        # Effectuer une requête POST vers la vue de réservation
        response = self.client.post(reverse('booking', kwargs={'pk': self.doctor.pk}), data=form_data)

        # Vérifier que la réponse a un code de statut réussi
        self.assertEqual(response.status_code, 302)  # 302 est le code de statut pour la redirection

        # Vérifier que le rendez-vous n'a pas été créé
        appointments = Appointment.objects.filter(patient=self.patient, doctor=self.doctor)
        self.assertEqual(appointments.count(), 0)

        # Vérifier que les détails du rendez-vous sont corrects
        appointment = appointments.first()
        self.assertIsNone(appointment)


class UnavailableDatesTestCase(unittest.TestCase):
    def test_get_unavailable_dates(self):
        doctor = Doctor.objects.create(last_name="Dr. John Doe")
        today = date.today()

        # Créer un DoctorTimeSlots avec des dates appropriées
        DoctorTimeSlots.objects.create(
            doctor=doctor,
            doc_start_date=today - timedelta(days=1),
            doc_end_date=today + timedelta(days=1)
        )

        # Créer un utilisateur
        user = User.objects.create(email="patients11@test.com")

        # Créer une instance de Patient correspondant à l'utilisateur
        patient = Patient.objects.create(user=user)

        # Créer des rendez-vous pour atteindre la limite quotidienne
        daily_quota = 5
        for _ in range(daily_quota):
            Appointment.objects.create(
                doctor=doctor,
                start_date=today - timedelta(days=1),
                end_date=today + timedelta(days=1),
                patient=patient  # Attribuer l'instance de Patient à l'objet Appointment
            )

    def test_get_unavailable_dates_no_slots(self):
        doctor = Doctor.objects.create(last_name="Dr. Jane Smith")
        today = date.today()

        # Exécuter la fonction get_unavailable_dates sans créer de DoctorTimeSlots
        unavailable_dates = get_unavailable_dates(doctor, today)

        # Vérifier que la liste des dates non disponibles est vide
        expected_unavailable_dates = []
        self.assertEqual(unavailable_dates, expected_unavailable_dates)

    def test_get_unavailable_dates_no_appointments(self):
        doctor = Doctor.objects.create(last_name="Dr. Alex Johnson")
        today = date.today()

        # Créer un DoctorTimeSlots avec des dates appropriées
        DoctorTimeSlots.objects.create(
            doctor=doctor,
            doc_start_date=today - timedelta(days=1),
            doc_end_date=today + timedelta(days=1)
        )

        # Exécuter la fonction get_unavailable_dates sans créer de rendez-vous
        unavailable_dates = get_unavailable_dates(doctor, today)

        # Vérifier que la liste des dates non disponibles est vide
        expected_unavailable_dates = []
        self.assertEqual(unavailable_dates, expected_unavailable_dates)



if __name__ == '__main__':
    unittest.main()