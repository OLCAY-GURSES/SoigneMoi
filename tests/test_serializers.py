from django.test import TestCase
from rest_framework.exceptions import ValidationError
from book.models import User, Admin, Hospital, Specialization, Patient, Doctor, DoctorTimeSlots, Appointment, Prescription, Prescription_medicine, Prescription_test, Test_Information, Secretary
from api.serializers import UserSerializer, AdminSerializer, HospitalSerializer, SpecializationSerializer, PatientSerializer, DoctorSerializer, DoctorTimeSlotsSerializer, AppointmentSerializer, PrescriptionMedicineSerializer, PrescriptionTestSerializer, TestInformationSerializer, PrescriptionSerializer

class SerializerTestCase(TestCase):

    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        self.user = User.objects.create_user(**self.user_data)

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
            first_name="Dr. Alice",
            last_name="Smith",
            specialization=self.specialization,
            phone_number="0987654321",
            date_of_birth="1980-01-01",
            reg_number="5678",
            hospital_name=self.hospital
        )

    def test_user_serializer(self):
        serializer = UserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data["email"], self.user_data["email"])

    def test_hospital_serializer(self):
        serializer = HospitalSerializer(self.hospital)
        data = serializer.data
        self.assertEqual(data["name"], self.hospital.name)

    def test_specialization_serializer(self):
        serializer = SpecializationSerializer(self.specialization)
        data = serializer.data
        self.assertEqual(data["specialization_name"], self.specialization.specialization_name)

    def test_patient_serializer(self):
        serializer = PatientSerializer(self.patient)
        data = serializer.data
        self.assertEqual(data["first_name"], self.patient.first_name)

    def test_doctor_serializer(self):
        serializer = DoctorSerializer(self.doctor)
        data = serializer.data
        self.assertEqual(data["first_name"], self.doctor.first_name)

    def test_doctor_time_slots_serializer(self):
        doctor_time_slots = DoctorTimeSlots.objects.create(
            doctor=self.doctor,
            doc_start_date="2024-07-01",
            doc_end_date="2024-07-31"
        )
        serializer = DoctorTimeSlotsSerializer(doctor_time_slots)
        data = serializer.data
        self.assertEqual(data["doctor"]["first_name"], self.doctor.first_name)

    def test_appointment_serializer(self):
        doctor_time_slots = DoctorTimeSlots.objects.create(
            doctor=self.doctor,
            doc_start_date="2024-07-01",
            doc_end_date="2024-07-31"
        )
        appointment = Appointment.objects.create(
            doctor_time_slots=doctor_time_slots,
            start_date="2024-07-10",
            end_date="2024-07-10",
            motif="Routine Checkup",
            doctor=self.doctor,
            patient=self.patient,
            serial_number="1234"
        )
        serializer = AppointmentSerializer(appointment)
        data = serializer.data
        self.assertEqual(data["motif"], appointment.motif)

    def test_prescription_medicine_serializer(self):
        prescription = Prescription.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            create_date="2024-07-10",
            extra_information="Take with food"
        )
        prescription_medicine = Prescription_medicine.objects.create(
            prescription=prescription,
            medicine_name="Aspirin",
            quantity="10",
            dosage="2 times a day",
            start_day="2024-07-10",
            end_day="2024-07-20",
            frequency="Daily",
            instruction="Take after meal"
        )
        serializer = PrescriptionMedicineSerializer(prescription_medicine)
        data = serializer.data
        self.assertEqual(data["medicine_name"], prescription_medicine.medicine_name)

    def test_prescription_test_serializer(self):
        prescription = Prescription.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            create_date="2024-07-10",
            extra_information="Take with food"
        )
        prescription_test = Prescription_test.objects.create(
            prescription=prescription,
            test_name="Blood Test",
            test_description="Full blood count",
            test_info_id="BT123",
            test_results="Normal"
        )
        serializer = PrescriptionTestSerializer(prescription_test)
        data = serializer.data
        self.assertEqual(data["test_name"], prescription_test.test_name)

    def test_test_information_serializer(self):
        test_information = Test_Information.objects.create(
            test_name="X-Ray",
            test_description="Chest X-Ray"
        )
        serializer = TestInformationSerializer(test_information)
        data = serializer.data
        self.assertEqual(data["test_name"], test_information.test_name)

    def test_prescription_serializer(self):
        prescription = Prescription.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            create_date="2024-07-10",
            extra_information="Take with food"
        )
        Prescription_medicine.objects.create(
            prescription=prescription,
            medicine_name="Aspirin",
            quantity="10",
            dosage="2 times a day",
            start_day="2024-07-10",
            end_day="2024-07-20",
            frequency="Daily",
            instruction="Take after meal"
        )
        Prescription_test.objects.create(
            prescription=prescription,
            test_name="Blood Test",
            test_description="Full blood count",
            test_info_id="BT123",
            test_results="Normal"
        )
        serializer = PrescriptionSerializer(prescription)
        data = serializer.data
        self.assertEqual(data["doctor"]["first_name"], self.doctor.first_name)
        self.assertEqual(data["patient"]["first_name"], self.patient.first_name)
        self.assertEqual(len(data["prescription_medicines"]), 1)
        self.assertEqual(data["prescription_medicines"][0]["medicine_name"], "Aspirin")
        self.assertEqual(len(data["prescription_test"]), 1)
        self.assertEqual(data["prescription_test"][0]["test_name"], "Blood Test")