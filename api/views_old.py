from datetime import timezone
from rest_framework import status, pagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from book.models import Doctor, Patient, Prescription, Prescription_medicine, Prescription_test
from .serializers import *


@api_view(['GET', 'POST'])
def hospital_list(request):
    if request.method == 'GET':
        hospitals = Hospital.objects.all()
        serializer = HospitalSerializer(hospitals, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def hospital_detail(request, pk):
    try:
        hospital = Hospital.objects.get(pk=pk)
    except Hospital.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HospitalSerializer(hospital)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = HospitalSerializer(hospital, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        hospital.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([])
def hospital_list_paged(request):
    paginator = pagination.PageNumberPagination()
    paginator.page_size = 3

    hospitals = Hospital.objects.all()
    result_page = paginator.paginate_queryset(hospitals, request)

    serializer = HospitalSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
def logout(request):
    # Invalidating the user's session
    request.session.flush()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data['user']
    login(request, user)

    return Response({'success': True})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_dashboard(request):
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


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def doctor_profile(request):
    doctor = Doctor.objects.get(user=request.user)

    if request.method == 'GET':
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    return Response({'message': 'Méthode non autorisée'}, status=405)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_prescription(request, patient_pk):
    doctor = Doctor.objects.get(user=request.user)
    patient = Patient.objects.get(pk=patient_pk)

    serializer = PrescriptionSerializer(
        data=request.data,
        context={'doctor': doctor, 'patient': patient}
    )

    if serializer.is_valid():
        prescription = serializer.save()

        medicines = request.data.get('medicines')
        tests = request.data.get('tests')

        if medicines:
            for medicine in medicines:
                PrescriptionMedicineSerializer().create(medicine, prescription=prescription)

        if tests:
            for test in tests:
                PrescriptionTestSerializer().create(test, prescription=prescription)

        return Response(PrescriptionSerializer(prescription).data)

    return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def view_prescription(request, pk):
    doctor = Doctor.objects.get(user=request.user)
    prescription = Prescription.objects.get(pk=pk)

    if request.method == 'GET':
        serializer = PrescriptionSerializer(
            prescription,
            context={'doctor': doctor}
        )
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PrescriptionSerializer(
            prescription,
            data=request.data,
            context={'doctor':doctor}
        )

        if serializer.is_valid():
            serializer.save()

            # Mettre à jour les médicaments/tests si nécessaire
            medicines = request.data.get('medicines')

            if medicines:
                for medicine_data in medicines:
                    try:
                        medicine = prescription.medicines.get(pk=medicine_data['id'])
                    except Prescription_medicine.DoesNotExist:
                        medicine = Prescription_medicine()

                    medicine_serializer = PrescriptionMedicineSerializer(
                        medicine, data=medicine_data
                    )

                    if medicine_serializer.is_valid():
                        medicine_serializer.save()

            tests = request.data.get('tests')

            if tests:
                for test_data in tests:
                    try:
                        test = prescription.tests.get(pk=test_data['id'])
                    except Prescription_test.DoesNotExist:
                        test = Prescription_test()

                    test_serializer = PrescriptionTestSerializer(
                        test, data=test_data
                    )

                    if test_serializer.is_valid():
                        test_serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=400)