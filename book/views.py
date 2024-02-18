from django.db.models import Count, Q
from django.utils import formats
from django.utils import timezone
from .forms import CustomUserCreationForm
from django.views.decorators.cache import cache_control
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from book.models import Patient, User, Hospital, Admin, Specialization, Doctor, Appointment, Prescription, \
    DoctorTimeSlots

from django.shortcuts import redirect, render
from .models import Doctor, Appointment

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
        context = {'patient': patient, 'appointments': appointments}
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
            age = request.POST.get('age')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')

            patient.first_name = first_name
            patient.last_name = last_name
            patient.date_of_bird = date_of_bird
            patient.age = age
            patient.phone_number = phone_number
            patient.address = address

            patient.save()

            messages.success(request, 'Sauvegarde confirmé')

            return redirect('patient-dashboard')
    else:
        redirect('logout')

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
@login_required(login_url="doctor-login")
def doctor_profile_settings(request):
    # profile_Settings.js
    if request.user.is_doctor:
        doctor = Doctor.objects.get(user=request.user)

        if request.method == 'GET':
            context = {'doctor': doctor}
            return render(request, 'book/doctors/doctor-profile-settings.html', context)

        elif request.method == 'POST':

            doc_first_name = request.POST.get('first_name')
            doc_last_name = request.POST.get('last_name')
            number = request.POST.get('number')
            date_of_bird = request.POST.get('date_of_bird')

            doctor.first_name = doc_first_name
            doctor.last_name = doc_last_name
            doctor.phone_number = number
            doctor.date_of_bird = date_of_bird

            doctor.save()

            # context = {'degree': degree}
            messages.success(request, 'Profile Mise à jour')
            return redirect('doctor-dashboard')
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

    if request.method == 'POST':
        appointment = Appointment(patient=patient, doctor=doctor)
        start_date = request.POST['appoint_start_date']
        end_date = request.POST['appoint_end_date']
        message = request.POST['message']

        """transformed_date_start = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        transformed_date_start = datetime.fromisoformat(transformed_date_start).date()

        transformed_date_end = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        transformed_date_end = datetime.fromisoformat(transformed_date_end).date()"""
        transformed_date_start = datetime.strptime(start_date, '%Y-%m-%d').date()
        transformed_date_end = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Check if the selected date is prior to the current date
        if transformed_date_start < date.today() or transformed_date_end < date.today():
            messages.error(request, 'Veuillez sélectionner une date à partir d\'aujourd\'hui ou ultérieure.')
            return redirect('booking', pk=pk)

        # Vérifier la présence du médecin (DoctorTimeSlots)
        is_present = DoctorTimeSlots.objects.filter(
            doctor=doctor,
            doc_start_date__lte=transformed_date_end,
            doc_end_date__gte=transformed_date_start
        ).exists()

        if not is_present:
            # Le médecin n'est pas présent pendant cette période
            messages.error(request, 'Le médecin n\'est pas présent pendant cette période.Merci de choisire une autre date.')
            return redirect('booking', pk=pk)

        # Vérifier le quota de patients par jour (DoctorTimeSlots)
        daily_quota = 5  # Le quota quotidien est fixé à 5 patients, vous pouvez le modifier si nécessaire
        patient_count = Appointment.objects.filter(
            doctor=doctor,
            start_date__lte=transformed_date_end,
            end_date__gte=transformed_date_start
        ).count()

        if patient_count >= daily_quota:
            # Le quota de patients pour cette journée a été atteint
            messages.error(request, 'Le médecin n\'est pas disponible aux dates choisies. Veuillez choisir une autre date. Le planning du médecin est rempli.')
            return redirect('booking', pk=pk)

        # Le médecin est présent et le quota n'a pas été atteint, enregistrer le rendez-vous
        appointment.start_date = transformed_date_start
        appointment.end_date = transformed_date_end

        appointment.serial_number = generate_random_string()

        appointment.message = message
        appointment.save()

        messages.success(request, 'Séjour réservé avec succès.')
        return redirect('patient-dashboard')

    next_available_date = get_next_available_date(doctor)
    if next_available_date:
        next_available_date_formatted = formats.date_format(next_available_date, format='j F Y')


    context = {'patient': patient, 'doctor': doctor,'next_available_date_formatted': next_available_date_formatted}
    return render(request, 'book/patient/booking.html', context)


def get_next_available_date(doctor):
    today = timezone.now().date()
    next_available_date = None
    delta = timedelta(days=1)

    while not next_available_date:
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

            if patient_count < daily_quota:
                next_available_date = today

        today += delta

    return next_available_date

