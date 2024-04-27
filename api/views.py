import datetime
from datetime import date
from rest_framework import viewsets, status

from rest_framework.authtoken.models import Token

from book.models import User, Admin, Hospital, Specialization, Patient, Doctor, DoctorTimeSlots, Appointment, Prescription, Prescription_medicine, Prescription_test, Test_Information, Secretary
from .serializers import UserSerializer, AdminSerializer, HospitalSerializer, SpecializationSerializer, \
    PatientSerializer, DoctorSerializer, DoctorTimeSlotsSerializer,  PrescriptionSerializer, \
    PrescriptionMedicineSerializer, PrescriptionTestSerializer, TestInformationSerializer,  \
    PatientProfileSerializer

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

from django.utils import timezone


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated]

class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated]

class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [IsAuthenticated]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

class DoctorTimeSlotsViewSet(viewsets.ModelViewSet):
    queryset = DoctorTimeSlots.objects.all()
    serializer_class = DoctorTimeSlotsSerializer
    permission_classes = [IsAuthenticated]


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all().order_by('-create_date')
    serializer_class = PrescriptionSerializer

class PrescriptionMedicineViewSet(viewsets.ModelViewSet):
    queryset = Prescription_medicine.objects.all()
    serializer_class = PrescriptionMedicineSerializer
    permission_classes = [IsAuthenticated]

class PrescriptionTestViewSet(viewsets.ModelViewSet):
    queryset = Prescription_test.objects.all()
    serializer_class = PrescriptionTestSerializer
    permission_classes = [IsAuthenticated]

class TestInformationViewSet(viewsets.ModelViewSet):
    queryset = Test_Information.objects.all()
    serializer_class = TestInformationSerializer
    permission_classes = [IsAuthenticated]


class PatientProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Updated import and class name

    def get(self, request, pk):
        doctor = None
        secretary = None
        prescription = None

        if request.user.is_doctor:
            doctor = get_object_or_404(Doctor, user=request.user)
            patient = get_object_or_404(Patient, patient_id=pk)
            appointments = Appointment.objects.filter(doctor=doctor, patient=patient)
            prescription = Prescription.objects.filter(doctor=doctor, patient=patient)
        elif request.user.is_secretary:
            secretary = get_object_or_404(Secretary, user=request.user)
            patient = get_object_or_404(Patient, patient_id=pk)
            appointments = Appointment.objects.filter(secretary=secretary, patient=patient)
        else:
            return Response({"detail": "Invalid user type"}, status=400)

        serializer = PatientProfileSerializer({
            'doctor': doctor,
            'appointments': appointments,
            'patient': patient,
            'prescription': prescription,
            'secretary': secretary
        })
        return Response(serializer.data)

class SecretaryDashboardView(APIView):
    permission_classes = [IsAuthenticated]  # Updated import and class name

    def get(self, request):
        current_date = date.today()

        start_appointments = Appointment.objects.filter(start_date=current_date)
        end_appointments = Appointment.objects.filter(end_date=current_date)

        start_patients = [PatientSerializer(appointment.patient).data for appointment in start_appointments]
        end_patients = [PatientSerializer(appointment.patient).data for appointment in end_appointments]

        data = {
            'start_patients': start_patients,
            'end_patients': end_patients
        }

        return Response(data)



class DoctorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_date = timezone.now().date()
        current_date_str = str(current_date)
        doctor = request.user.profile  # Récupérer l'instance Doctor associée à l'utilisateur authentifié
        today_appointments = Appointment.objects.filter(start_date__lte=current_date, end_date__gte=current_date, doctor=doctor)
        today_appointments_data = []

        for appointment in today_appointments:
            patient_first_name = f"{appointment.patient.first_name} "
            patient_last_name = f" {appointment.patient.last_name}"
            patient_phone_number = f"{appointment.patient.phone_number} "
            patient_address = f"{appointment.patient.address} "
            patient_date_of_birth = f"{appointment.patient.date_of_birth} "

            appointment_data = {
                'start_date': str(appointment.start_date),
                'end_date': str(appointment.end_date),
                'motif': appointment.motif,
                'serial_number': appointment.serial_number,
                'patient_id': appointment.patient.patient_id,
                'patient_first_name': patient_first_name,
                'patient_last_name': patient_last_name,
                'patient_phone_number': patient_phone_number,
                'patient_address': patient_address,
                'patient_date_of_birth': patient_date_of_birth,
            }
            today_appointments_data.append(appointment_data)

        data = {
            'today_appointments': today_appointments_data,
            'current_date': current_date_str,
            'doctor_id': doctor.doctor_id,  # Ajouter l'ID du docteur
        }
        return Response(data)


class CreatePrescriptionView(APIView):
    def post(self, request, pk):
        # Check if the logged-in user is a doctor
        if request.user.is_doctor:
            # Retrieve the doctor from the logged-in user
            doctor = Doctor.objects.get(user=request.user)
            # Retrieve the patient from the provided ID
            patient = Patient.objects.get(patient_id=pk)
            # Define the creation date of the prescription
            create_date = timezone.now().date()

            # Create a new prescription
            prescription = Prescription(doctor=doctor, patient=patient)

            # Retrieve the prescription data from the request
            medicine_data = request.data.get('prescription_medicines', [])
            extra_information = request.data.get('extra_information', '')

            # Fill in the prescription fields
            prescription.extra_information = extra_information
            prescription.create_date = create_date
            prescription.save()

            # Save the prescription medicines
            if medicine_data:
                for medicine in medicine_data:
                    medicine_obj = Prescription_medicine(prescription=prescription)
                    medicine_obj.medicine_name = medicine.get('medicine_name', '')
                    medicine_obj.quantity = medicine.get('quantity', '')
                    medicine_obj.dosage = medicine.get('dosage', '')
                    medicine_obj.frequency = medicine.get('frequency', '')
                    # Convert the start and end dates of the treatment
                    start_day_str = medicine.get('start_day', '')
                    end_day_str = medicine.get('end_day', '')
                    if start_day_str:
                        medicine_obj.start_day = datetime.strptime(start_day_str, '%d/%m/%Y').date()
                    if end_day_str:
                        medicine_obj.end_day = datetime.strptime(end_day_str, '%d/%m/%Y').date()
                    medicine_obj.instruction = medicine.get('instruction', '')
                    medicine_obj.save()

            # Save the prescription tests
            test_data = request.data.get('prescription_test', [])
            if test_data:
                for test in test_data:
                    test_obj = Prescription_test(prescription=prescription)
                    test_obj.test_name = test.get('test_name', '')
                    test_obj.test_description = test.get('test_description', '')
                    test_obj.save()

            # Return the data of the created prescription
            serializer = PrescriptionSerializer(prescription)
            return Response(serializer.data, status=201)

        # If the user is not a doctor, return an access denied message
        return Response({'detail': 'Access denied.'}, status=403)

class DoctorViewPrescription(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        doctor = Doctor.objects.get(user=request.user)
        prescription = get_object_or_404(Prescription, prescription_id=pk)
        serializer = PrescriptionSerializer(prescription)
        return Response(serializer.data)

    def post(self, request, pk):
        doctor = Doctor.objects.get(user=request.user)
        prescription = get_object_or_404(Prescription, prescription_id=pk)
        medicines = Prescription_medicine.objects.filter(prescription=prescription)
        tests = Prescription_test.objects.filter(prescription=prescription)

        if request.method == 'POST':
            medicines_end_day = request.data.get('end_day')
            # Convert end_day to datetime object
            end_day = datetime.strptime(medicines_end_day, '%d/%m/%Y').date()

            # Trouver l'instance de Prescription_medicine que vous souhaitez modifier
            prescription_medicine_id = request.data.get('prescription_medicine_id')
            prescription_medicine = Prescription_medicine.objects.get(pk=prescription_medicine_id)

            # Mettre à jour la valeur de end_day de l'instance de Prescription_medicine
            prescription_medicine.end_day = end_day
            prescription_medicine.save()

            serializer = PrescriptionSerializer(prescription)
            return Response(serializer.data)

        serializer = PrescriptionSerializer(prescription)
        return Response(serializer.data)


class DoctorUpdateMedicineEndDate(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, prescription_id, prescription_medicine_id):
        # Récupérer l'instance de Prescription_medicine
        prescription_medicine = get_object_or_404(Prescription_medicine, prescription__prescription_id=prescription_id, medicine_id=prescription_medicine_id)

        # Mettre à jour end_day à partir de request.data
        end_day = request.data.get('end_day')
        if end_day:
            prescription_medicine.end_day = datetime.strptime(end_day, "%Y-%m-%d").date()
            prescription_medicine.save()

        serializer = PrescriptionMedicineSerializer(prescription_medicine)
        return Response(serializer.data)



class ObtainAuthTokenView(APIView):
    throttle_classes = []
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        is_secretary = user.is_secretary
        is_doctor = user.is_doctor

        # Récupérer l'instance Doctor associée à l'utilisateur
        doctor = None
        if is_doctor:
            doctor = Doctor.objects.get(user=user)
            doctor_id = doctor.doctor_id

        return Response({'token': token.key, 'is_secretary': is_secretary, 'is_doctor': is_doctor,
                         'doctor_id': doctor_id if is_doctor else None})
