<<<<<<< HEAD

from .serializers import PatientSerializer, UserLoginSerializer, UserSerializer

from django.contrib.auth import logout
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from book.models import User, Appointment, Doctor, Prescription, Secretary
from rest_framework.permissions import BasePermission, AllowAny
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import serializers
from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from book.models import Patient, Appointment
from datetime import date

#from sgm_api.serializers import PatientSerializer, AppointmentSerializer




class UserTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserTokenRefreshView(TokenRefreshView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer


class UserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            if user.is_patient:
                role = 'is_patient'
            elif user.is_doctor:
                role = 'is_doctor'
            elif user.is_secretary:
                role = 'is_secretary'
            else:
                role = 'unknown'

            response_data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'role': role
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:

            return Response({'message': 'Nom d\'utilisateur ou mot de passe incorrect'}, status=status.HTTP_401_UNAUTHORIZED)


def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Vous avez été déconnecté avec succès.'})

"""class SecretaryDashboardAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_secretary:
            current_date = date.today()

            start_appointments = Appointment.objects.filter(start_date=current_date)
            end_appointments = Appointment.objects.filter(end_date=current_date)

            start_patients = PatientSerializer(start_appointments, many=True).data
            end_patients = PatientSerializer(end_appointments, many=True).data

            data = {
                'start_patients': start_patients,
                'end_patients': end_patients
            }

            return Response(data)
        else:
            return Response({'message': 'Unauthorized'}, status=401)"""

class SecretaryDashboardAPIView(APIView):

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


=======
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
        today_appointments = Appointment.objects.filter(start_date__lte=current_date, end_date__gte=current_date)
        today_appointments_data = []

        for appointment in today_appointments:
            patient_first_name = f"{appointment.patient.first_name} "
            patient_last_name = f" {appointment.patient.last_name}"
            patient_phone_number = f"{appointment.patient.phone_number} "
            patient_address = f"{appointment.patient.address} "
            appointment_data = {
                'start_date': str(appointment.start_date),
                'end_date': str(appointment.end_date),
                'motif': appointment.motif,
                'serial_number': appointment.serial_number,
                #'doctor_time_slots': appointment.doctor_time_slots.id,
                'patient_id': appointment.patient.patient_id,
                'patient_first_name': patient_first_name,
                'patient_last_name': patient_last_name,
                'patient_phone_number': patient_phone_number,
                'patient_address': patient_address,
            }
            today_appointments_data.append(appointment_data)

        data = {
            'today_appointments': today_appointments_data,
            'current_date': current_date_str,
        }
        return Response(data)

class CreatePrescriptionView(APIView):
    def post(self, request, pk):
        if request.user.is_doctor:
            doctor = Doctor.objects.get(user=request.user)
            patient = Patient.objects.get(patient_id=pk)
            create_date = timezone.now().date()

            prescription = Prescription(doctor=doctor, patient=patient)

            medicine_data = request.data.get('prescription_medicines', [])
            extra_information = request.data.get('extra_information', '')

            prescription.extra_information = extra_information
            prescription.create_date = create_date
            prescription.save()

            if medicine_data:
                for medicine in medicine_data:
                    medicine_obj = Prescription_medicine(prescription=prescription)
                    medicine_obj.medicine_name = medicine.get('medicine_name', '')
                    medicine_obj.quantity = medicine.get('quantity', '')
                    medicine_obj.frequency = medicine.get('frequency', '')

                    start_day_str = medicine.get('start_day', '')
                    end_day_str = medicine.get('end_day', '')

                    if start_day_str:
                        medicine_obj.start_day = datetime.strptime(start_day_str, '%d/%m/%Y').date()

                    if end_day_str:
                        medicine_obj.end_day = datetime.strptime(end_day_str, '%d/%m/%Y').date()

                    medicine_obj.instruction = medicine.get('instruction', '')
                    medicine_obj.save()

            test_data = request.data.get('prescription_test', [])
            if test_data:
                for test in test_data:
                    test_obj = Prescription_test(prescription=prescription)
                    test_obj.test_name = test.get('test_name', '')
                    test_obj.test_description = test.get('test_description', '')
                    test_obj.save()

            serializer = PrescriptionSerializer(prescription)
            return Response(serializer.data, status=201)

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
        return Response({'token': token.key, 'is_secretary': is_secretary,'is_doctor': is_doctor})
>>>>>>> 3a1623a302e78e3b2b97c1e2eafd76799e3410af
