from django.contrib.auth import  authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from book.forms import CustomUserCreationForm
from book.models import Hospital, User, Patient, Doctor


# Create your views here.

@csrf_exempt
def home(request):
    hospitals = Hospital.objects.all()
    doctors = Doctor.objects.all()
    context = {'hospitals': hospitals,'doctors':doctors}
    return render(request, 'book/home.html', context)


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

        context = {'patient': patient}
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
            # doctor = Doctor_Information.objects.get(user_id=pk)
            doctor = Doctor.objects.get(user=request.user)
            pass

        else:
            return redirect('logout')

        context = {'doctor': doctor}
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

