import os
import unittest
from django.test import TestCase
from django.contrib.auth import get_user_model
from book.models import *

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sgm_system.settings")
import django
django.setup()

User = get_user_model()

class ModelTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.admin = Admin.objects.create(user=self.user)
        self.hospital = Hospital.objects.create(name='Test Hospital', address='123 Test Street')
        self.specialization = Specialization.objects.create(hospital=self.hospital, specialization_name='Cardiology')
        self.patient = Patient.objects.create(user=self.user, first_name='John', last_name='Doe', phone_number='1234567890', address='123 Test Address', date_of_birth=date(1990, 1, 1), serial_number='ABC123')
        self.doctor = Doctor.objects.create(user=self.user, first_name='Jane', last_name='Smith', specialization=self.specialization, phone_number='0987654321', date_of_birth=date(1985, 5, 5), reg_number='123456', hospital_name=self.hospital)
        self.doctor_time_slots = DoctorTimeSlots.objects.create(doctor=self.doctor, doc_start_date=date(2023, 4, 1), doc_end_date=date(2023, 4, 30))
        self.appointment = Appointment.objects.create(doctor_time_slots=self.doctor_time_slots, start_date=date(2023, 4, 15), end_date=date(2023, 4, 15), motif='Routine checkup', doctor=self.doctor, patient=self.patient, serial_number='XYZ789', choise_speciality=self.specialization)
        self.prescription = Prescription.objects.create(doctor=self.doctor, patient=self.patient, create_date=date(2023, 4, 15), extra_information='Take medication as directed')
        self.prescription_medicine = Prescription_medicine.objects.create(prescription=self.prescription, medicine_name='Aspirin', quantity='100mg', dosage='1 tablet per day', start_day=date(2023, 4, 15), end_day=date(2023, 4, 22), frequency='Daily', instruction='Take with food')
        self.prescription_test = Prescription_test.objects.create(prescription=self.prescription, test_name='Blood test', test_description='Complete blood count', test_info_id='ABC123', test_results='Normal')
        self.test_information = Test_Information.objects.create(test_name='Blood test', test_description='Complete blood count')
        self.secretary = Secretary.objects.create(user=self.user, first_name='John', last_name='Doe', phone_number='1234567890', address='123 Test Address', date_of_birth=date(1990, 1, 1), reg_number='123456', hospital_name=self.hospital)

    def test_user_model(self):
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('testpassword'))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_admin)
        self.assertFalse(self.user.is_patient)
        self.assertFalse(self.user.is_doctor)
        self.assertFalse(self.user.is_secretary)
        self.assertFalse(self.user.login_status)

    def test_admin_model(self):
        self.assertEqual(self.admin.user, self.user)

    def test_hospital_model(self):
        self.assertEqual(self.hospital.name, 'Test Hospital')
        self.assertEqual(self.hospital.address, '123 Test Street')

    def test_specialization_model(self):
        self.assertEqual(self.specialization.specialization_name, 'Cardiology')
        self.assertEqual(self.specialization.hospital, self.hospital)

    def test_patient_model(self):
        self.assertEqual(self.patient.user, self.user)
        self.assertEqual(self.patient.first_name, 'John')
        self.assertEqual(self.patient.last_name, 'Doe')
        self.assertEqual(self.patient.phone_number, '1234567890')
        self.assertEqual(self.patient.address, '123 Test Address')
        self.assertEqual(self.patient.date_of_birth, date(1990, 1, 1))
        self.assertEqual(self.patient.serial_number, 'ABC123')

    def test_doctor_model(self):
        self.assertEqual(self.doctor.user, self.user)
        self.assertEqual(self.doctor.first_name, 'Jane')
        self.assertEqual(self.doctor.last_name, 'Smith')
        self.assertEqual(self.doctor.specialization, self.specialization)
        self.assertEqual(self.doctor.phone_number, '0987654321')
        self.assertEqual(self.doctor.date_of_birth, date(1985, 5, 5))
        self.assertEqual(self.doctor.reg_number, '123456')
        self.assertEqual(self.doctor.hospital_name, self.hospital)

    def test_doctor_time_slots_model(self):
        self.assertEqual(self.doctor_time_slots.doctor, self.doctor)
        self.assertEqual(self.doctor_time_slots.doc_start_date, date(2023, 4, 1))
        self.assertEqual(self.doctor_time_slots.doc_end_date, date(2023, 4, 30))

    def test_appointment_model(self):
        self.assertEqual(self.appointment.doctor_time_slots, self.doctor_time_slots)
        self.assertEqual(self.appointment.start_date, date(2023, 4, 15))
        self.assertEqual(self.appointment.end_date, date(2023, 4, 15))
        self.assertEqual(self.appointment.motif, 'Routine checkup')
        self.assertEqual(self.appointment.doctor, self.doctor)
        self.assertEqual(self.appointment.patient, self.patient)
        self.assertEqual(self.appointment.serial_number, 'XYZ789')
        self.assertEqual(self.appointment.choise_speciality, self.specialization)

    def test_prescription_model(self):
        self.assertEqual(self.prescription.doctor, self.doctor)
        self.assertEqual(self.prescription.patient, self.patient)
        self.assertEqual(self.prescription.create_date, date(2023, 4, 15))
        self.assertEqual(self.prescription.extra_information, 'Take medication as directed')

    def test_prescription_medicine_model(self):
        self.assertEqual(self.prescription_medicine.prescription, self.prescription)
        self.assertEqual(self.prescription_medicine.medicine_name, 'Aspirin')
        self.assertEqual(self.prescription_medicine.quantity, '100mg')
        self.assertEqual(self.prescription_medicine.dosage, '1 tablet per day')
        self.assertEqual(self.prescription_medicine.start_day, date(2023, 4, 15))
        self.assertEqual(self.prescription_medicine.end_day, date(2023, 4, 22))
        self.assertEqual(self.prescription_medicine.frequency, 'Daily')
        self.assertEqual(self.prescription_medicine.instruction, 'Take with food')

    def test_prescription_test_model(self):
        self.assertEqual(self.prescription_test.prescription, self.prescription)
        self.assertEqual(self.prescription_test.test_name, 'Blood test')
        self.assertEqual(self.prescription_test.test_description, 'Complete blood count')
        self.assertEqual(self.prescription_test.test_info_id, 'ABC123')
        self.assertEqual(self.prescription_test.test_results, 'Normal')

    def test_test_information_model(self):
        self.assertEqual(self.test_information.test_name, 'Blood test')
        self.assertEqual(self.test_information.test_description, 'Complete blood count')

    def test_secretary_model(self):
        self.assertEqual(self.secretary.user, self.user)
        self.assertEqual(self.secretary.first_name, 'John')
        self.assertEqual(self.secretary.last_name, 'Doe')
        self.assertEqual(self.secretary.phone_number, '1234567890')
        self.assertEqual(self.secretary.address, '123 Test Address')
        self.assertEqual(self.secretary.date_of_birth, date(1990, 1, 1))
        self.assertEqual(self.secretary.reg_number, '123456')
        self.assertEqual(self.secretary.hospital_name, self.hospital)

if __name__ == '__main__':
    unittest.main()
