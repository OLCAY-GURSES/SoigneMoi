from django.db.models import Count, Q
from django.http import HttpResponseBadRequest, HttpResponse
from django.urls import reverse
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from book.models import Patient, User, Hospital, Admin, Specialization, Doctor, Appointment, Prescription, \
    DoctorTimeSlots, Prescription_test, Prescription_medicine, Secretary

from django.shortcuts import redirect, render

from django.db.models import Count, F
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import datetime, date, timedelta
from .signals import generate_random_string
from .utils import paginateHospitals


# Create your views here.
class HomeView(View):
    def get(self, request):
        self.hospitals = Hospital.objects.all()
        context = {'hospitals': self.hospitals}
        return render(request, 'book/home.html', context)

class ListHospitalView(View):
    def get(self, request):
        self.hospitals = Hospital.objects.all()
        self.custom_range, self.hospitals = paginateHospitals(request, self.hospitals, 3)
        context = {'hospitals': self.hospitals, 'custom_range': self.custom_range}
        return render(request, 'book/administration/list-hospital.html', context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Utilisateur déconnecté')
        return redirect('login')

class LoginView(View):
    def get(self, request):
        self.page = 'login'
        return render(request, 'book/login.html')

    def post(self, request):
        self.email = request.POST['email']
        self.password = request.POST['password']

        try:
            self.user = User.objects.get(email=self.email)
        except User.DoesNotExist:
            messages.error(request, "Adresse e-mail ou mot de passe incorrect", extra_tags='danger')
            return render(request, 'book/login.html')

        self.user = authenticate(email=self.email, password=self.password)

        if self.user is not None:
            login(request, self.user)
            if request.user.is_patient:
                messages.success(request, "Utilisateur connecté avec succès")
                return redirect('patient-dashboard')
            elif request.user.is_admin:
                messages.success(request, "Administrateur connecté avec succès")
                return redirect('/')
            else:
                messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page", extra_tags='danger')
                return render(request, 'book/login.html')
        else:
            messages.error(request, "Adresse e-mail ou mot de passe incorrect", extra_tags='danger')
            return render(request, 'book/login.html')
class PatientRegisterView(View):
    def get(self, request):
        self.page = 'patient-register'
        self.form = CustomUserCreationForm()
        context = {'page': self.page, 'form': self.form}
        return render(request, 'book/patient/patient-register.html', context)

    def post(self, request):
        self.form = CustomUserCreationForm(request.POST)
        if self.form.is_valid():
            self.user = self.form.save(commit=False)
            self.user.is_patient = True
            self.user.save()
            messages.success(request, "Le compte patient a été créé !")
            return redirect('login')
        else:
            messages.error(request, "Une erreur s'est produite lors de l'enregistrement!")
        context = {'form': self.form}
        return render(request, 'book/patient/patient-register.html', context)

class PatientDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_patient:
            self.patient = Patient.objects.get(user=request.user)
            self.appointments = Appointment.objects.filter(patient=self.patient).order_by('-start_date')
            self.prescription = Prescription.objects.filter(patient=self.patient).order_by('-prescription_id')
            context = {'patient': self.patient, 'appointments': self.appointments, 'prescription': self.prescription}
        else:
            return redirect('logout')
        return render(request, 'book/patient/patient-dashboard.html', context)



class ProfileSettingsView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_patient:
            self.patient = Patient.objects.get(user=request.user)
            context = {'patient': self.patient}
            return render(request, 'book/patient/profile-settings.html', context)
        else:
            return redirect('logout')

    def post(self, request):
        if request.user.is_patient:
            self.patient = Patient.objects.get(user=request.user)
            self.first_name = request.POST.get('first_name')
            self.last_name = request.POST.get('last_name')
            self.date_of_birth_str = request.POST.get('date_of_birth')
            self.phone_number = request.POST.get('phone_number')
            self.address = request.POST.get('address')

            if not self.date_of_birth_str:
                messages.error(request, "La date de naissance est manquante.")
                return redirect('profile-settings')

            try:
                self.date_of_birth = datetime.strptime(self.date_of_birth_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, "Le format de la date de naissance doit être aaaa-mm-jj.")
                return redirect('profile-settings')

            self.patient.first_name = self.first_name
            self.patient.last_name = self.last_name
            self.patient.date_of_birth = self.date_of_birth
            self.patient.phone_number = self.phone_number
            self.patient.address = self.address
            self.patient.save()

            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('patient-dashboard')
        else:
            return redirect('logout')

class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            self.patient = Patient.objects.get(user_id=pk)
            context = {"patient": self.patient}
            return render(request, 'book/password/change-password.html', context)
        except Patient.DoesNotExist:
            messages.error(request, "Utilisateur introuvable.")
            return render(request, 'book/password/change-password.html', {'messages': messages.get_messages(request)})

    def post(self, request, pk):
        try:
            self.patient = Patient.objects.get(user_id=pk)
            self.old_password = request.POST["old_password"]
            self.new_password = request.POST["new_password"]
            self.confirm_password = request.POST["confirm_password"]

            if request.user.check_password(self.old_password):
                if self.new_password == self.confirm_password:
                    request.user.set_password(self.new_password)
                    request.user.save()
                    messages.success(request, "Le mot de passe a été modifié avec succès")
                    # Connecter l'utilisateur avec le nouveau mot de passe
                    user = authenticate(username=request.user.username, password=self.new_password)
                    if user is not None:
                        login(request, user)
                    # Rediriger vers la page de connexion
                    return redirect('login')
                else:
                    messages.error(request, "Le nouveau mot de passe et le mot de passe de confirmation ne sont pas identiques")
            else:
                messages.error(request, "L'ancien mot de passe est incorrect")

            return render(request, 'book/password/change-password.html', {'patient': self.patient, 'messages': messages.get_messages(request)})
        except Patient.DoesNotExist:
            messages.error(request, "Utilisateur introuvable.")
            return render(request, 'book/password/change-password.html', {'messages': messages.get_messages(request)})
class SearchView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_patient:
            self.search_query = request.GET.get('search_query', '')
            self.doctors = Doctor.objects.filter(
                Q(last_name__icontains=self.search_query) |
                Q(first_name__icontains=self.search_query) |
                Q(specialization__specialization_name__icontains=self.search_query)
            )
            self.patient = Patient.objects.get(user=request.user)
            context = {'patient': self.patient, 'doctors': self.doctors, 'search_query': self.search_query}
            return render(request, 'book/patient/search.html', context)
        else:
            logout(request)
            messages.error(request, 'Non autorisé')
            return render(request, 'login.html')

class BookingView(LoginRequiredMixin, View):
    def get(self, request, pk):
        self.patient = request.user.patient
        self.doctor = Doctor.objects.get(doctor_id=pk)

        # Check if profile settings are filled
        if not (self.patient.first_name and self.patient.last_name and self.patient.date_of_birth and self.patient.phone_number and self.patient.address):
            messages.error(request, 'Veuillez remplir tous les champs de votre profil avant de réserver.')
            return redirect('profile-settings')

        self.unavailable_dates = self.get_unavailable_dates(self.doctor)
        context = {'patient': self.patient, 'doctor': self.doctor, 'unavailable_dates': self.unavailable_dates}
        return render(request, 'book/patient/booking.html', context)

    def post(self, request, pk):
        self.patient = request.user.patient
        self.doctor = Doctor.objects.get(doctor_id=pk)

        self.appointment = Appointment(patient=self.patient, doctor=self.doctor)
        self.start_date = datetime.strptime(request.POST['appoint_start_date'], '%Y-%m-%d').date()
        self.end_date = datetime.strptime(request.POST['appoint_end_date'], '%Y-%m-%d').date()
        self.message = request.POST.get('message', '')

        if not self.message:
            messages.error(request, 'Veuillez saisir un motif pour votre rendez-vous.')
            return redirect('booking', pk=pk)

        if self.start_date < date.today():
            messages.error(request, 'Veuillez sélectionner une date de début à partir d\'aujourd\'hui ou ultérieure.')
            return redirect('booking', pk=pk)

        if self.start_date >= self.end_date:
            messages.error(request, 'La date de début de séjour doit être antérieure à la date de fin de séjour.')
            return redirect('booking', pk=pk)

        self.current_date = self.start_date
        while self.current_date <= self.end_date:
            self.is_present = DoctorTimeSlots.objects.filter(
                doctor=self.doctor,
                doc_start_date__lte=self.current_date,
                doc_end_date__gte=self.current_date
            ).exists()

            if not self.is_present:
                messages.error(request, 'Le médecin n\'est pas présent pendant la période sélectionnée. Veuillez choisir une autre période.')
                return redirect('booking', pk=pk)

            self.daily_quota = 5
            self.patient_count = Appointment.objects.filter(
                doctor=self.doctor,
                start_date__lte=self.current_date,
                end_date__gte=self.current_date
            ).count()

            if self.patient_count >= self.daily_quota:
                messages.error(request, 'Le médecin n\'est pas disponible aux dates choisies. Veuillez sélectionner une autre date. Le planning du médecin est complet pour les jours suivants :')
                self.booking_url = reverse('booking', args=[pk])
                return redirect(f'{self.booking_url}?dates_displayed=True')

            self.current_date += timedelta(days=1)

        self.appointment.start_date = self.start_date
        self.appointment.end_date = self.end_date
        self.appointment.serial_number = generate_random_string()
        self.appointment.message = self.message
        self.appointment.save()

        messages.success(request, 'Séjour réservé avec succès.')
        return redirect('patient-dashboard')

    def get_unavailable_dates(self, doctor):
        self.unavailable_dates = []
        today = date.today()
        self.end_date = today + timedelta(days=365)
        self.delta = timedelta(days=1)

        while today <= self.end_date:
            self.is_present = DoctorTimeSlots.objects.filter(
                doctor=doctor,
                doc_start_date__lte=today,
                doc_end_date__gte=today
            ).exists()

            if self.is_present:
                self.daily_quota = 5
                self.patient_count = Appointment.objects.filter(
                    doctor=doctor,
                    start_date__lte=today,
                    end_date__gte=today
                ).count()

                if self.patient_count >= self.daily_quota:
                    self.unavailable_dates.append(today)

            today += self.delta

        return self.unavailable_dates

class PrescriptionView(LoginRequiredMixin, View):
    def get(self, request, pk):
        if request.user.is_patient:
            self.patient = Patient.objects.get(user=request.user)
            self.prescription = Prescription.objects.filter(prescription_id=pk)
            self.prescription_medicine = Prescription_medicine.objects.filter(prescription__in=self.prescription)
            self.prescription_test = Prescription_test.objects.filter(prescription__in=self.prescription)

            context = {
                'patient': self.patient,
                'prescription': self.prescription,
                'prescription_test': self.prescription_test,
                'prescription_medicine': self.prescription_medicine
            }
            return render(request, 'book/patient/prescription-view.html', context)
        else:
            return redirect('logout')
