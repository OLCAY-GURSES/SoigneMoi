from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Remplacez `book` par le nom de votre application si nécessaire
from book.models import Hospital, Specialization, Patient, Doctor, Prescription, Prescription_medicine, Prescription_test

User = get_user_model()

class TemplateTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="password123")
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            address="123 Test St",
            email="hospital@example.com",
            phone_number="1234567890"
        )
        self.specialization = Specialization.objects.create(
            hospital=self.hospital,
            specialization_name="Cardiology"
        )
        self.patient = Patient.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            phone_number="1234567890",
            address="123 Test St",
            date_of_birth="2000-01-01",
            serial_number="1234"
        )
        self.doctor = Doctor.objects.create(
            user=self.user,
            specialization=self.specialization,
            first_name="Dr. Alice",
            last_name="Smith",
            phone_number="0987654321",
            date_of_birth="1980-01-01",
            reg_number="5678",
            hospital_name=self.hospital
        )
        self.prescription = Prescription.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            create_date="2024-07-10",
            extra_information="Take with food"
        )
        self.prescription_medicine = Prescription_medicine.objects.create(
            prescription=self.prescription,
            medicine_name="Aspirin",
            quantity="10",
            dosage="2 times a day",
            start_day="2024-07-10",
            end_day="2024-07-20",
            frequency="Daily",
            instruction="Take after meal"
        )
        self.prescription_test = Prescription_test.objects.create(
            prescription=self.prescription,
            test_name="Blood Test",
            test_description="Full blood count",
            test_info_id="BT123",
            test_results="Normal"
        )

    def test_hospital_list_template(self):
        response = self.client.get(reverse('hospital_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/hospital_list.html')
        self.assertContains(response, "Test Hospital")

    def test_patient_detail_template(self):
        response = self.client.get(reverse('patient_detail', args=[self.patient.id]))  #
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/patient_detail.html')
        self.assertContains(response, "John Doe")
        self.assertContains(response, "123 Test St")

    def test_doctor_detail_template(self):
        response = self.client.get(reverse('doctor_detail', args=[self.doctor.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/doctor_detail.html')
        self.assertContains(response, "Dr. Alice Smith")
        self.assertContains(response, "Cardiology")

    def test_prescription_detail_template(self):
        response = self.client.get(reverse('prescription_detail', args=[self.prescription.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/prescription_detail.html')
        self.assertContains(response, "Aspirin")
        self.assertContains(response, "Blood Test")