from datetime import date
from urllib import request

from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserLoginSerializer, AppointmentSerializer, DoctorSerializer, PrescriptionSerializer, \
    UserSerializer, SecretarySerializer
from book.models import Doctor, Appointment, Patient, Prescription, Prescription_medicine, Prescription_test, User
from django.contrib.auth import login
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny



class LogoutView(viewsets.ModelViewSet):
    def create(self, request):
        # Invalidating the user's session
        request.session.flush()
        return Response(status=status.HTTP_200_OK)


class IsDoctor(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_doctor


class IsSecretary(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_secretary

class LoginView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsDoctor]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                # Authentification réussie
                # Effectuer d'autres opérations nécessaires
                return Response({'success': True})
            else:
                # Mot de passe incorrect
                return Response({'success': False, 'message': 'Invalid password'})
        except User.DoesNotExist:
            # Utilisateur non trouvé
            return Response({'success': False, 'message': 'User not found'})

class DoctorDashboardView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer
    permission_classes = [IsDoctor]

    def list(self, request, *args, **kwargs):
        doctor = Doctor.objects.get(user=request.user)
        today = timezone.now().date()
        appointments = Appointment.objects.filter(
            start_date__lte=today,
            end_date__gte=today,
            doctor=doctor
        )

        serializer = AppointmentSerializer(appointments, many=True)

        return Response({
            'doctor': DoctorSerializer(doctor).data,
            'today': today,
            'appointments': serializer.data
        })
class DoctorProfileView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DoctorSerializer  # Remplacez DoctorSerializer par votre sérialiseur approprié
    permission_classes = [IsDoctor]

    def get_queryset(self):
        return Doctor.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class CreatePrescriptionView(viewsets.ModelViewSet):
    queryset = Prescription.objects.none()  # Crée un queryset vide
    permission_classes = [IsAuthenticated]
    serializer_class = PrescriptionSerializer
    permission_classes = [IsDoctor]



class ViewPrescriptionView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Prescription.objects.all()  # Spécifiez la queryset appropriée
    serializer_class = PrescriptionSerializer
    permission_classes = [IsDoctor]

    def perform_create(self, serializer):
        doctor = Doctor.objects.get(user=self.request.user)
        serializer.save(doctor=doctor)

    def perform_update(self, serializer):
        doctor = Doctor.objects.get(user=self.request.user)
        serializer.save(doctor=doctor)


class SecretaryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SecretarySerializer
    queryset = Appointment.objects.all()
    permission_classes = [IsSecretary]

    def list(self, request):
        current_date = date.today()

        start_appointments = Appointment.objects.filter(start_date=current_date)
        end_appointments = Appointment.objects.filter(end_date=current_date)

        start_patients = [appointment.patient for appointment in start_appointments]
        end_patients = [appointment.patient for appointment in end_appointments]

        start_patients_data = self.serializer_class(start_patients, many=True).data
        end_patients_data = self.serializer_class(end_patients, many=True).data

        context = {
            'start_patients': start_patients_data,
            'end_patients': end_patients_data
        }

        return Response(context)