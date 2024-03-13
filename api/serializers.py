from rest_framework import serializers
from book.models import User, Admin, Hospital, Specialization, Patient, Doctor, DoctorTimeSlots,\
    Appointment, Prescription, Prescription_medicine, Prescription_test, Test_Information, Secretary


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = '__all__'

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

class SpecializationSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer()

    class Meta:
        model = Specialization
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class DoctorTimeSlotsSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()

    class Meta:
        model = DoctorTimeSlots
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class PrescriptionMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription_medicine
        fields = ['medicine_id', 'medicine_name', 'quantity', 'start_day', 'end_day', 'frequency', 'instruction']

class PrescriptionTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription_test
        fields = ['test_id', 'test_name', 'test_description', 'test_info_id']

class TestInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test_Information
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    patient = PatientSerializer()
    prescription_medicines = PrescriptionMedicineSerializer(many=True)
    prescription_test = PrescriptionTestSerializer(many=True)


    class Meta:
        model = Prescription
        fields = '__all__'

class PatientProfileSerializer(serializers.Serializer):
    doctor = serializers.SerializerMethodField()

    patient = serializers.SerializerMethodField()
    appointments = AppointmentSerializer(many=True)
    prescription = PrescriptionSerializer(many=True)

    def get_doctor(self, obj):
        if 'doctor' in obj:
            return DoctorSerializer(obj['doctor']).data
        return None



    def get_patient(self, obj):
        if 'patient' in obj:
            return PatientSerializer(obj['patient']).data
        return None



"""class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'is_admin', 'is_patient', 'is_doctor', 'is_secretary', 'login_status']"""



"""class PrescriptionSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    patient = PatientSerializer()

    class Meta:
        model = Prescription
        fields = '__all__'"""


"""class PatientProfileSerializer(serializers.Serializer):
    appointments = AppointmentSerializer(many=True)
    prescriptions = PrescriptionSerializer(many=True)

    def get_prescriptions(self, obj):
        if obj.get('prescription'):
            serializer = PrescriptionSerializer(obj['prescription'], many=True)
            return serializer.data
        return []

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['prescriptions'] = self.get_prescriptions(data)
        return data
"""

"""class PatientProfileSerializer(serializers.Serializer):
    doctor = DoctorSerializer(read_only=True)
    appointments = AppointmentSerializer(many=True, read_only=True)
    patient = PatientSerializer(read_only=True)
    prescription = serializers.SerializerMethodField()
    secretary = serializers.SerializerMethodField()

    def get_prescription(self, obj):
        if obj.get('prescription'):
            # Serialize Prescription objects here if needed
            return obj['prescription']
        return []

    def get_secretary(self, obj):
        if obj.get('secretary'):
            # Serialize Secretary object here if needed
            return obj['secretary']
        return None"""