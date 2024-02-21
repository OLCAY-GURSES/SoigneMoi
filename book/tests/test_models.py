import os
import django

# Configurer les paramètres Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgm_system.settings')
django.setup()

import unittest
from django.contrib.auth import get_user_model
from django.test import TestCase
from book.models import Hospital, Specialization, Patient, Admin, Appointment, DoctorTimeSlots, Doctor, \
    Prescription_test, Test_Information, Prescription, Prescription_medicine

User = get_user_model()



class TestModels(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        email = "test1@example.com"
        password = "testpass123"
        user = self.User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_patient)
        self.assertFalse(user.is_doctor)
        self.assertFalse(user.login_status)

    def test_create_superuser(self):
        email = "admin@example.com"
        password = "adminpass123"
        user = self.User.objects.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_admin)
        self.assertFalse(user.is_patient)
        self.assertFalse(user.is_doctor)
        self.assertFalse(user.login_status)


class HospitalModelTest(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(
            name='Hospital A',
            address='123 Main Street',
            featured_image='hospitals/hospital_a.png',
            description='This is Hospital A',
            email='hospitala@example.com',
            phone_number='1234567890'
        )

    def test_create_hospital(self):
        hospital = Hospital.objects.create(
            name='Test Hospital',
            address='123 Test Street',
            email='info@testhospital.com',
            phone_number='1234567890'
        )
        self.assertEqual(hospital.name, 'Test Hospital')
        self.assertEqual(hospital.address, '123 Test Street')
        self.assertEqual(hospital.email, 'info@testhospital.com')
        self.assertEqual(hospital.phone_number, '1234567890')

    def test_str_representation(self):
        self.assertEqual(str(self.hospital), 'Hospital A')

class AdminModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='admin@example.com')
        self.admin = Admin.objects.create(user=self.user)

    def test_str_representation(self):
        self.assertEqual(str(self.admin), 'admin@example.com')


class SpecializationModelTest(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(
            name='Hospital',
            address='Address',
            email='hospital@example.com',
            phone_number='1234567890'
        )
        self.specialization = Specialization.objects.create(
            hospital=self.hospital,
            specialization_name='Specialization'
        )

    def test_create_specialization(self):
        hospital = Hospital.objects.create(
            name='Test Hospital',
            address='123 Test Street',
            email='info@testhospital.com',
            phone_number='1234567890'
        )
        specialization = Specialization.objects.create(
            specialization_name='Test Specialization',
            hospital=hospital
        )
        self.assertEqual(specialization.specialization_name, 'Test Specialization')
        self.assertEqual(specialization.hospital, hospital)


    def test_str_representation(self):
        expected_str = 'Specialization - Hospital'
        self.assertEqual(str(self.specialization), expected_str)


class PatientModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='patient@example.com')
        self.patient = Patient.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            phone_number='1234567890',
            address='Address',
            date_of_bird='2000-01-01',
            serial_number='ABC123'
        )
    def test_create_patient(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            password='password'
        )



        patient = Patient.objects.create(
            user=user,
            first_name='John',
            last_name='Doe',
            phone_number='1234567890',
            address='456 Test Street',
            serial_number='ABC123'
        )
        self.assertEqual(patient.user, user)
        self.assertEqual(patient.first_name, 'John')
        self.assertEqual(patient.last_name, 'Doe')
        self.assertEqual(patient.phone_number, '1234567890')
        self.assertEqual(patient.address, '456 Test Street')
        self.assertEqual(patient.serial_number, 'ABC123')

    def test_str_representation(self):
        self.assertEqual(str(self.patient), 'patient@example.com')


class AppointmentModelTest(TestCase):
    def setUp(self):
        doctor = Doctor.objects.create(
            user=User.objects.create(email='doctor@example.com'),
            first_name='John',
            last_name='Doe',
            phone_number='1234567890'
        )
        patient = Patient.objects.create(
            user=User.objects.create( email='patient@example.com'),
            first_name='Jane',
            last_name='Doe',
            phone_number='1234567890',
            address='Address',
            date_of_bird='2000-01-01',
            serial_number='ABC123'
        )
        doctor_time_slots = DoctorTimeSlots.objects.create(
            doctor=doctor,
            doc_start_date='2022-01-01',
            doc_end_date='2022-01-02'
        )
        specialization = Specialization.objects.create(specialization_name='Specialization')
        hospital = Hospital.objects.create(name='Hospital', address='Address')

        self.appointment = Appointment.objects.create(
            doctor_time_slots=doctor_time_slots,
            start_date='2022-01-01',
            end_date='2022-01-02',
            motif='Motif',
            doctor=doctor,
            patient=patient,
            serial_number='ABC123',
            choise_speciality=specialization
        )

    def test_str_representation(self):
        self.assertEqual(str(self.appointment), 'Doe')


class PrescriptionMedicineModelTest(TestCase):
    def setUp(self):
        doctor = Doctor.objects.create(
            first_name='John',
            last_name='Doe'
        )
        patient = Patient.objects.create(
            first_name='Jane',
            last_name='Doe'
        )
        prescription = Prescription.objects.create(
            doctor=doctor,
            patient=patient,
            create_date='2022-01-01',
            medicine_name='Medicine',
            quantity='1',
            days='7',
            time='Morning',
            medicine_description='Description',
            test_name='Test',
            test_description='Test Description',
            extra_information='Extra Information'
        )
        self.prescription_medicine = Prescription_medicine.objects.create(
            prescription=prescription,
            medicine_name='Medicine',
            quantity='1',
            start_day='2022-01-01',
            end_day='2022-01-07',
            frequency='Once a day',
            instruction='Take with water'
        )

    def test_create_prescription_medicine(self):
        self.assertEqual(self.prescription_medicine.prescription.doctor.first_name, 'John')
        self.assertEqual(self.prescription_medicine.prescription.patient.last_name, 'Doe')
        self.assertEqual(self.prescription_medicine.medicine_name, 'Medicine')
        self.assertEqual(self.prescription_medicine.quantity, '1')
        self.assertEqual(self.prescription_medicine.start_day, '2022-01-01')
        self.assertEqual(self.prescription_medicine.end_day, '2022-01-07')
        self.assertEqual(self.prescription_medicine.frequency, 'Once a day')
        self.assertEqual(self.prescription_medicine.instruction, 'Take with water')

    def test_str_representation(self):
        expected_representation = str(self.prescription_medicine.prescription.prescription_id)
        self.assertEqual(str(self.prescription_medicine), expected_representation)


class PrescriptionTestModelTest(TestCase):
    def setUp(self):
        doctor = Doctor.objects.create(
            first_name='John',
            last_name='Doe'
        )
        patient = Patient.objects.create(
            first_name='Jane',
            last_name='Doe'
        )
        prescription = Prescription.objects.create(
            doctor=doctor,
            patient=patient,
            create_date='2022-01-01',
            medicine_name='Medicine',
            quantity='1',
            days='7',
            time='Morning',
            medicine_description='Description',
            test_name='Test',
            test_description='Test Description',
            extra_information='Extra Information'
        )
        self.prescription_test = Prescription_test.objects.create(
            prescription=prescription,
            test_name='Test',
            test_description='Test Description',
            test_info_id='12345'
        )

    def test_create_prescription_test(self):
        self.assertEqual(self.prescription_test.prescription.doctor.first_name, 'John')
        self.assertEqual(self.prescription_test.prescription.patient.last_name, 'Doe')
        self.assertEqual(self.prescription_test.test_name, 'Test')
        self.assertEqual(self.prescription_test.test_description, 'Test Description')
        self.assertEqual(self.prescription_test.test_info_id, '12345')

    def test_str_representation(self):
        expected_representation = str(self.prescription_test.prescription.prescription_id)
        self.assertEqual(str(self.prescription_test), expected_representation)


class TestInformationModelTest(TestCase):
    def setUp(self):
        self.test_information = Test_Information.objects.create(
            test_name='Test'
        )

    def test_create_test_information(self):
        self.assertEqual(self.test_information.test_name, 'Test')

    def test_str_representation(self):
        self.assertEqual(str(self.test_information), 'Test')


if __name__ == '__main__':
    unittest.main()