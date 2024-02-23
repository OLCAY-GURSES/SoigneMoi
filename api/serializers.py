from rest_framework import serializers
from book.models import User, Admin, Hospital, Specialization, Patient, Doctor, DoctorTimeSlots, Appointment, \
    Prescription, Prescription_medicine, Prescription_test, Test_Information, Secretary
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = []


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    prescription_id = serializers.IntegerField()  # Ajoutez ce champ explicite

    class Meta:
        model = Prescription
        fields = '__all__'

class SecretarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Secretary
        fields = '__all__'
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.login_status:
                    user.login_status = True
                    user.save()
                return user
            else:
                raise serializers.ValidationError('Unable to login with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')