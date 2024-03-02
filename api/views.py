
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


