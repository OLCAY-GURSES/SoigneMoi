from django.db.models import Count, Q
from django.http import HttpResponseBadRequest, HttpResponse
from django.urls import reverse
from django.utils import timezone
from .forms import CustomUserCreationForm
from django.views.decorators.cache import cache_control
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from book.models import Patient, User, Hospital, Admin, Specialization, Doctor, Appointment, Prescription, \
    DoctorTimeSlots, Prescription_test, Prescription_medicine, Secretary

from django.shortcuts import redirect, render
import datetime

from django.db.models import Count, F
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import datetime, date, timedelta
from .signals import generate_random_string
from .utils import paginateHospitals
# Create your views here.

@csrf_exempt
def home(request):
    hospitals = Hospital.objects.all()
    context = {'hospitals': hospitals}
    return render(request, 'book/home.html', context)


@csrf_exempt
def list_hospital(request):
    hospitals = Hospital.objects.all()
    custom_range, hospitals = paginateHospitals(request, hospitals, 3)

    context = {'hospitals': hospitals,'custom_range': custom_range}
    return render(request, 'book/administration/list-hospital.html', context)


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True)
def logoutUser(request):
    logout(request)
    messages.success(request, 'Utilisateur déconnecté')
    return redirect('login')


@csrf_exempt
def login_user(request):
    page = 'login'
    if request.method == 'GET':
        return render(request, 'book/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            pass

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_patient:
                messages.success(request, "L'utilisateur s'est connecté avec succès")
                return redirect('patient-dashboard')
            if request.user.is_doctor:
                messages.success(request, 'Bonjour Docteur')
                return redirect('doctor-dashboard')
            if request.user.is_secretary:
                messages.success(request, 'Bonjour secretaire')
                return redirect('secretary_list')

            else:
                messages.error(request, "Informations d'identification non valides.")
                return redirect('logout')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")

    return render(request, 'book/login.html')


@csrf_exempt
def patient_register(request):
    page = 'patient-register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # form.save()
            user = form.save(
                commit=False)  # commit=False --> don't save to database yet (we have a chance to modify object)
            user.is_patient = True
            user.save()
            messages.success(request, "Le compte patient a été créé !")

            # After user is created, we can log them in --> login(request, user)
            return redirect('login')

        else:
            messages.error(request, "Une erreur s'est produite lors de l'enregistrement!")

    context = {'page': page, 'form': form}
    return render(request, 'book/patient/patient-register.html', context)


@csrf_exempt
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def patient_dashboard(request):
    if request.user.is_patient:
        patient = Patient.objects.get(user=request.user)
        appointments = Appointment.objects.filter(patient=patient).order_by('-start_date')
        prescription = Prescription.objects.filter(patient=patient).order_by('-prescription_id')
        context = {'patient': patient, 'appointments': appointments,
                   'prescription': prescription}
    else:
        return redirect('logout')

    return render(request, 'book/patient/patient-dashboard.html', context)


@csrf_exempt
@login_required(login_url="login")
def profile_settings(request):
    if request.user.is_patient:
        patient = Patient.objects.get(user=request.user)

        if request.method == 'GET':
            context = {'patient': patient}
            return render(request, 'book/patient/profile-settings.html', context)

        elif request.method == 'POST':

            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            date_of_bird = request.POST.get('date_of_bird')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')

            if not date_of_bird:
                return HttpResponseBadRequest("L'âge est manquant.")


                # Convertir la date de naissance en objet date en utilisant le format spécifié
                date_of_bird = datetime.strptime(date_of_bird, '%d/%m/%Y').date()


            patient.first_name = first_name
            patient.last_name = last_name
            patient.date_of_bird = date_of_bird
            patient.phone_number = phone_number
            patient.address = address

            patient.save()

            messages.success(request, 'Sauvegarde confirmé')

            return redirect('patient-dashboard')

    else:
        return redirect('logout')

@csrf_exempt
@login_required(login_url="login")
def change_password(request, pk):
    patient = Patient.objects.get(user_id=pk)
    context = {"patient": patient}
    if request.method == "POST":
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]
        if new_password == confirm_password:

            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "Le mot de passe a été modifié avec succès")
            return redirect("patient-dashboard")
        else:
            messages.error(request, "Le nouveau mot de passe et le mot de passe de confirmation ne sont pas identiques")
            return redirect("change-password", pk)
    return render(request, 'book/password/change-password.html', context)



@csrf_exempt
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True)
def doctor_dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_doctor:

            if request.user.is_authenticated:
                if request.user.is_doctor:
                    # doctor = Doctor_Information.objects.get(user_id=pk)
                    doctor = Doctor.objects.get(user=request.user)
                    #current_date = datetime.date.today()
                    current_date=timezone.now().date()
                    current_date_str = str(current_date)
                    # today_appointments = Appointment.objects.filter(doctor_time_slots__start_date__lte=current_date,doctor_time_slots__end_date__gte=current_date, doctor=doctor)
                    today_appointments = Appointment.objects.filter(start_date__lte=current_date, end_date__gte=current_date, doctor=doctor)

                else:
                    return redirect('doctor-logout')

                context = {'doctor': doctor,
                           'today_appointments': today_appointments,
                           'current_date': current_date_str,
                           }
                return render(request, 'book/doctors/doctor-dashboard.html', context)
    else:
        return redirect('login')



@csrf_exempt
@login_required(login_url="login")
def doctor_profile_settings(request):
    # profile_Settings.js
    if request.user.is_doctor:
        doctor = Doctor.objects.get(user=request.user)

        if request.method == 'GET':
            context = {'doctor': doctor}
            return render(request, 'book/doctors/doctor-profile-settings.html', context)

    else:
        redirect('logout')



@csrf_exempt
@login_required(login_url="login")
def search(request):
    if request.user.is_authenticated and request.user.is_patient:

        search_query = ''

        if request.GET.get('search_query'):
            search_query = request.GET.get('search_query')

        doctors = Doctor.objects.filter(
            Q(last_name__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(specialization__specialization_name__icontains=search_query)

        )

        patient = Patient.objects.get(user=request.user)
        context = {'patient': patient, 'doctors': doctors,  'search_query': search_query}
        return render(request, 'book/doctors/search.html', context)
    else:
        logout(request)
        messages.error(request, 'Non autorisé')
        return render(request, 'login.html')

@csrf_exempt
@login_required(login_url="doctor-login")
def booking(request, pk):
    patient = request.user.patient
    doctor = Doctor.objects.get(doctor_id=pk)
    # Check if profile settings are filled
    if not (
            patient.first_name and patient.last_name and patient.date_of_bird and patient.phone_number and patient.address):
        messages.error(request, 'Veuillez remplir tous les champs de votre profil avant de réserver.')
        return redirect('profile-settings')

    if request.method == 'POST':
        appointment = Appointment(patient=patient, doctor=doctor)
        start_date = datetime.strptime(request.POST['appoint_start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.POST['appoint_end_date'], '%Y-%m-%d').date()
        message = request.POST['message']

        if start_date < date.today() or end_date < date.today():
            messages.error(request, 'Veuillez sélectionner une date à partir d\'aujourd\'hui ou ultérieure.')
            return redirect('booking', pk=pk)

        current_date = start_date
        while current_date <= end_date:
            is_present = DoctorTimeSlots.objects.filter(
                doctor=doctor,
                doc_start_date__lte=current_date,
                doc_end_date__gte=current_date
            ).exists()

            if not is_present:
                messages.error(request, 'Le médecin n\'est pas présent pendant la période sélectionnée. Veuillez choisir une autre période.')
                return redirect('booking', pk=pk)

            daily_quota = 5
            patient_count = Appointment.objects.filter(
                doctor=doctor,
                start_date__lte=current_date,
                end_date__gte=current_date
            ).count()

            if patient_count >= daily_quota:
                messages.error(request, 'Le médecin n\'est pas disponible aux dates choisies. Veuillez sélectionner une autre date. Le planning du médecin est complet pour les jours suivants :')
                booking_url = reverse('booking', args=[pk])
                return redirect(f'{booking_url}?dates_displayed=True')

            current_date += timedelta(days=1)

        appointment.start_date = start_date
        appointment.end_date = end_date
        appointment.serial_number = generate_random_string()
        appointment.message = message
        appointment.save()

        messages.success(request, 'Séjour réservé avec succès.')
        return redirect('patient-dashboard')

    unavailable_dates = get_unavailable_dates(doctor, date.today())
    context = {'patient': patient, 'doctor': doctor, 'unavailable_dates': unavailable_dates}
    return render(request, 'book/patient/booking.html', context)

def get_unavailable_dates(doctor, today):
    unavailable_dates = []

    end_date = today + timedelta(days=365)
    delta = timedelta(days=1)

    while today <= end_date:
        is_present = DoctorTimeSlots.objects.filter(
            doctor=doctor,
            doc_start_date__lte=today,
            doc_end_date__gte=today
        ).exists()

        if is_present:
            daily_quota = 5
            patient_count = Appointment.objects.filter(
                doctor=doctor,
                start_date__lte=today,
                end_date__gte=today
            ).count()

            if patient_count >= daily_quota:
                unavailable_dates.append(today)

        today += delta

    return unavailable_dates


@csrf_exempt
@login_required(login_url="login")
def patient_profile(request, pk):
    doctor = None  # Définir la variable doctor à l'extérieur de la condition
    secretary = None  # Définir la variable secretary à l'extérieur de la condition
    prescription = None  # Définir la variable prescription à l'extérieur de la condition

    if request.user.is_doctor:
        doctor = Doctor.objects.get(user=request.user)
        patient = Patient.objects.get(patient_id=pk)
        appointments = Appointment.objects.filter(doctor=doctor, patient=patient)
        prescription = Prescription.objects.filter(doctor=doctor, patient=patient)
    elif request.user.is_secretary:
        secretary = Secretary.objects.get(user=request.user)
        patient = Patient.objects.get(patient_id=pk)
        appointments = Appointment.objects.filter(secretary=secretary, patient=patient)
    else:
        return redirect('logout')

    context = {
        'doctor': doctor,
        'appointments': appointments,
        'patient': patient,
        'prescription': prescription,
        'secretary': secretary
    }
    return render(request, 'book/doctors/patient-profile.html', context)


@csrf_exempt
@login_required(login_url="login")
def create_prescription(request, pk):

    if request.user.is_doctor:
        doctor = Doctor.objects.get(user=request.user)
        patient = Patient.objects.get(patient_id=pk)
        create_date = timezone.now().date()

        if request.method == 'POST':
            prescription = Prescription(doctor=doctor, patient=patient)

            test_name = request.POST.getlist('test_name')
            test_description = request.POST.getlist('description')
            medicine_name = request.POST.getlist('medicine_name')
            medicine_quantity = request.POST.getlist('quantity')

            medecine_frequency = request.POST.getlist('frequency')
            medicine_start_day = request.POST.getlist('start_day')
            medicine_end_day = request.POST.getlist('end_day')

            medicine_instruction = request.POST.getlist('instruction')
            extra_information = request.POST.get('extra_information')


            prescription.extra_information = extra_information
            prescription.create_date = create_date


            prescription.save()

            for i in range(len(medicine_name)):
                medicine = Prescription_medicine(prescription=prescription)
                medicine.medicine_name = medicine_name[i]
                medicine.quantity = medicine_quantity[i]
                medicine.frequency = medecine_frequency[i]

                # Convert start_day and end_day to datetime objects
                start_day = datetime.strptime(medicine_start_day[i], '%d/%m/%Y').date()
                end_day = datetime.strptime(medicine_end_day[i], '%d/%m/%Y').date()

                medicine.start_day = start_day
                medicine.end_day = end_day
                medicine.instruction = medicine_instruction[i]

                medicine.save()

            for i in range(len(test_name)):
                tests = Prescription_test(prescription=prescription)
                tests.test_name = test_name[i]
                tests.test_description = test_description[i]


                tests.save()

            messages.success(request, 'Prescription Created')
            return redirect('patient-profile', pk=patient.patient_id)

    context = {'doctor': doctor, 'patient': patient, }
    return render(request, 'book/doctors/create-prescription.html', context)


@csrf_exempt
@login_required(login_url="login")
def doctor_view_prescription(request, pk):
    if request.user.is_authenticated and request.user.is_doctor:
        doctor = Doctor.objects.get(user=request.user)
        prescription = Prescription.objects.get(prescription_id=pk)
        medicines = Prescription_medicine.objects.filter(prescription=prescription)
        tests = Prescription_test.objects.filter(prescription=prescription)

        if request.method == 'POST':
            medicines_end_day = request.POST.get('end_day')
            # Convert end_day to datetime object
            end_day = datetime.strptime(medicines_end_day, '%d/%m/%Y').date()

            # Trouver l'instance de Prescription_medicine que vous souhaitez modifier
            prescription_medicine_id = request.POST.get('prescription_medicine_id')
            prescription_medicine = Prescription_medicine.objects.get(pk=prescription_medicine_id)

            # Mettre à jour la valeur de end_day de l'instance de Prescription_medicine
            prescription_medicine.end_day = end_day
            prescription_medicine.save()



        context = {'prescription': prescription, 'medicines': medicines, 'tests': tests, 'doctor': doctor}
        return render(request, 'book/doctors/doctor-view-prescription.html', context)



@csrf_exempt
@login_required(login_url="login")
def prescription_view(request, pk):
    if request.user.is_patient:
        patient = Patient.objects.get(user=request.user)
        prescription = Prescription.objects.filter(prescription_id=pk)
        prescription_medicine = Prescription_medicine.objects.filter(prescription__in=prescription)
        prescription_test = Prescription_test.objects.filter(prescription__in=prescription)

        context = {
            'patient': patient,
            'prescription': prescription,
            'prescription_test': prescription_test,
            'prescription_medicine': prescription_medicine
        }
        return render(request, 'book/patient/prescription-view.html', context)
    else:
        return redirect('logout')

@csrf_exempt
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True)
def nurse_dashboard(request):
    current_date = date.today()

    start_appointments = Appointment.objects.filter(start_date=current_date)
    end_appointments = Appointment.objects.filter(end_date=current_date)



    start_patients = [appointment.patient for appointment in start_appointments]
    end_patients = [appointment.patient for appointment in end_appointments]



    context = {
        'start_patients': start_patients, 'end_patients':end_patients
    }

    return render(request, 'book/secretary/secretary_list.html', context)