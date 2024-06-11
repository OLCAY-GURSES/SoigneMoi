import random

from django.db.models import Count, Q
from django.http import HttpResponseBadRequest, HttpResponse
from django.urls import reverse
import string
from django.views import View
from django.views.generic import ListView

from .forms import CustomUserCreationForm, DoctorForm, EditDoctorForm, ChangePasswordForm, DoctorScheduleForm, \
    SecretaryForm, EditSecretaryForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from book.models import Patient, User, Hospital, Admin, Specialization, Doctor, Appointment, Prescription, \
    DoctorTimeSlots, Prescription_test, Prescription_medicine, Secretary

from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

from django.db.models import Count, F
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import datetime, date, timedelta
from .signals import generate_random_string
from .utils import paginateHospitals
from django.db import transaction, IntegrityError

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
            return render(request, 'book/login.html')

class BookingView(LoginRequiredMixin, View):
    def get(self, request, pk):
        self.patient = request.user.patient
        self.doctor = Doctor.objects.get(doctor_id=pk)

        # Check if profile settings are filled
        if not (
                self.patient.first_name and self.patient.last_name and self.patient.date_of_birth and self.patient.phone_number and self.patient.address):
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
        self.motif = request.POST.get('motif', '')

        if not self.motif:
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
                messages.error(request,
                               'Le médecin n\'est pas présent pendant la période sélectionnée. Veuillez choisir une autre période.')
                return redirect('booking', pk=pk)

            self.daily_quota = 5
            self.patient_count = Appointment.objects.filter(
                doctor=self.doctor,
                start_date__lte=self.current_date,
                end_date__gte=self.current_date
            ).count()

            if self.patient_count >= self.daily_quota:
                messages.error(request,
                               'Le médecin n\'est pas disponible aux dates choisies. Veuillez sélectionner une autre date. Le planning du médecin est complet pour les jours suivants :')
                self.booking_url = reverse('booking', args=[pk])
                return redirect(f'{self.booking_url}?dates_displayed=True')

            self.current_date += timedelta(days=1)

        self.appointment.start_date = self.start_date
        self.appointment.end_date = self.end_date
        self.appointment.serial_number = generate_random_string()
        self.appointment.motif = self.motif
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


class AdminDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_admin:
            doctors = Doctor.objects.all()
            patients = Patient.objects.all()
            hospitals = Hospital.objects.all()
            secretarys = Secretary.objects.all()

            context = {
                'doctors': doctors,
                'patients': patients,
                'hospitals': hospitals,
                'secretarys':secretarys,
            }
            return render(request, 'book/administration/admin-dashboard.html', context)
        elif request.user.is_secretary:
            messages.error(request, 'Vous n\'êtes pas autorisé à accéder à cette page ')
            return redirect('secretary-dashboard')
        else:
            messages.error(request, 'Vous n\'êtes pas autorisé à accéder à cette page')
            return redirect('login')


class HospitalCreateView(LoginRequiredMixin, View):
    template_name = 'book/administration/hospital/add-hospital.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if request.user.is_admin:
            hospital = Hospital()
            featured_image = request.FILES.get('featured_image', "departments/default.png")
            hospital_name = request.POST.get('hospital_name')
            address = request.POST.get('address')
            description = request.POST.get('description')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            specialization_names = request.POST.getlist('specialization')

            hospital.name = hospital_name
            hospital.description = description
            hospital.address = address
            hospital.email = email
            hospital.phone_number = phone_number
            hospital.featured_image = featured_image
            hospital.save()

            for specialization_name in specialization_names:
                Specialization.objects.create(hospital=hospital, specialization_name=specialization_name)

            messages.success(request, 'Hôpital créé')
            return redirect('hospital-list')
        else:
            messages.error(request, 'Vous n\'êtes pas autorisé à ajouter un hôpital')
            return redirect('login')

class HospitalListView(LoginRequiredMixin, View):
    template_name = 'book/administration/hospital/hospital-list.html'
    def get(self, request, *args, **kwargs):
        hospitals = Hospital.objects.all()
        context = {'hospitals': hospitals}
        return render(request, self.template_name, context)


class HospitalUpdateView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'book/administration/hospital/edit-hospital.html'

    def get(self, request, pk, *args, **kwargs):
        if request.user.is_admin:
            hospital = get_object_or_404(Hospital, hospital_id=pk)
            specializations = Specialization.objects.filter(hospital=hospital)
            context = {'hospital': hospital, 'specializations': specializations}
            return render(request, self.template_name, context)
        else:
            messages.error(request, 'Vous n\'êtes pas autorisé à modifier cet hôpital')
            return redirect('login')

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_admin:
            hospital = get_object_or_404(Hospital, hospital_id=pk)
            old_featured_image = hospital.featured_image
            featured_image = request.FILES.get('featured_image', old_featured_image)

            hospital_name = request.POST.get('hospital_name')
            address = request.POST.get('address')
            description = request.POST.get('description')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            specialization_ids = request.POST.getlist('specialization_id')
            specialization_names = request.POST.getlist('specialization_name')
            new_specializations = request.POST.getlist('new_specializations[]')

            hospital.name = hospital_name
            hospital.description = description
            hospital.address = address
            hospital.email = email
            hospital.phone_number = phone_number
            hospital.featured_image = featured_image
            hospital.save()

            # Supprimer les spécialisations supprimées
            existing_specializations = Specialization.objects.filter(hospital=hospital)
            for specialization in existing_specializations:
                if str(specialization.specialization_id) not in specialization_ids:
                    specialization.delete()

            # Mettre à jour les spécialisations existantes
            for specialization_id, specialization_name in zip(specialization_ids, specialization_names):
                specialization = get_object_or_404(Specialization, specialization_id=specialization_id)
                specialization.specialization_name = specialization_name
                specialization.save()

            # Ajouter les nouvelles spécialités dynamiques
            for new_specialization in new_specializations:
                if new_specialization:
                    Specialization.objects.create(hospital=hospital, specialization_name=new_specialization)

            messages.success(request, 'Hôpital mis à jour')
            return redirect('hospital-list')
        else:
            messages.error(request, 'Vous n\'êtes pas autorisé à modifier cet hôpital')
            return redirect('login')

class HospitalDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        if request.user.is_admin:
            hospital = get_object_or_404(Hospital, hospital_id=pk)
            hospital.delete()
            messages.success(request, 'Hôpital supprimé')
            return redirect('hospital-list')
        else:
            messages.error(request, 'Vous n\'êtes pas autorisé à supprimer cet hôpital')
            return redirect('login')

class SpecializationDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk, pk2, *args, **kwargs):
        if request.user.is_admin:
            specialization = get_object_or_404(Specialization, specialization_id=pk)
            specialization.delete()
            messages.success(request, 'Spécialisation supprimée')
            return redirect('edit-hospital', pk=pk2)
        else:
            messages.error(request, 'Vous n\'êtes pas autorisé à supprimer cette spécialisation')
            return redirect('login')

class CreateDoctorView(LoginRequiredMixin, View):
    def get(self, request):
        hospitals = Hospital.objects.all()
        hospital_specializations = {
            hospital.hospital_id: list(
                hospital.specialization_set.values('specialization_id', 'specialization_name')
            )
            for hospital in hospitals
        }

        form = DoctorForm()
        context = {
            'form': form,
            'hospital_specializations': hospital_specializations
        }
        return render(request, 'book/administration/doctor/create-doctor.html', context)

    def post(self, request):
        form = DoctorForm(request.POST)
        if form.is_valid():
            specialization_id = form.cleaned_data['specialization'].specialization_id
            try:
                specialization = Specialization.objects.get(specialization_id=specialization_id)
            except Specialization.DoesNotExist:
                form.add_error('specialization', 'La spécialisation sélectionnée est invalide.')
            else:
                # Générer un numéro d'enregistrement unique
                reg_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                while Doctor.objects.filter(reg_number=reg_number).exists():
                    reg_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

                doctor = form.save(commit=False)
                doctor.reg_number = reg_number

                # Créer un nouvel utilisateur

                user = User.objects.create_user(

                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password1']
                )
                doctor.user = user

                doctor.save()

                doctor.user.is_doctor = True
                doctor.user.save()

                # Attribuer le rôle 'is_doctor'
                doctor_group, created = Group.objects.get_or_create(name='is_doctor')
                doctor.user.groups.add(doctor_group)

                messages.success(request, 'Le médecin a été créé avec succès.')
                return redirect('doctor-list')
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')

        hospitals = Hospital.objects.all()
        hospital_specializations = {
            hospital.hospital_id: list(
                hospital.specialization_set.values('specialization_id', 'specialization_name')
            )
            for hospital in hospitals
        }

        return render(request, 'book/administration/doctor/create-doctor.html', {
            'form': form,
            'hospital_specializations': hospital_specializations
        })


class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'book/administration/doctor/doctor-list.html'
    context_object_name = 'doctors'

    def get(self, request, *args, **kwargs):
        doctor_updated_success = request.session.pop('doctor_updated_success', False)
        password_changed_success = request.session.pop('password_changed_success', False)

        if doctor_updated_success:
            messages.success(request, "Les informations du médecin ont été mises à jour.")

        if password_changed_success:
            messages.success(request, "Le mot de passe du médecin a été modifié avec succès.")

        return super().get(request, *args, **kwargs)

class DeleteDoctorView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            doctor = Doctor.objects.get(doctor_id=pk)
            doctor_name = f"{doctor.first_name} {doctor.last_name}"
            doctor.delete()
            messages.success(request, f"Le médecin {doctor_name} a été supprimé avec succès.")
        except Doctor.DoesNotExist:
            messages.error(request, f"Le médecin avec l'ID {pk} n'existe pas.")
        return redirect('doctor-list')

class EditDoctorView(LoginRequiredMixin, View):
    def get(self, request, doctor_id):
        doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
        form = EditDoctorForm(instance=doctor)
        password_form = ChangePasswordForm(doctor.user)
        return render(request, 'book/administration/doctor/edit-doctor.html', {
            'form': form,
            'doctor': doctor,
            'password_form': password_form,
        })

    def post(self, request, doctor_id):
        doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
        form = EditDoctorForm(request.POST, instance=doctor)

        if form.is_valid():
            doctor = form.save(commit=False)
            user = doctor.user
            user.email = form.cleaned_data['email']
            user.save()
            doctor.save()
            request.session['doctor_updated_success'] = True
            return redirect('doctor-list')
        else:
            messages.error(request, "Erreur de mise à jour des informations. Veuillez vérifier les champs.")
            password_form = ChangePasswordForm(doctor.user)

        return render(request, 'book/administration/doctor/edit-doctor.html', {
            'form': form,
            'doctor': doctor,
            'password_form': password_form,
        })


class ChangeDoctorPasswordView(LoginRequiredMixin, View):
    def get(self, request, doctor_id):
        doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
        user = doctor.user
        form = ChangePasswordForm(user)
        return render(request, 'book/administration/doctor/change-doctor-password.html', {
            'form': form,
            'doctor': doctor,
        })

    def post(self, request, doctor_id):
        doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
        user = doctor.user
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            request.session['password_changed_success'] = True
            return redirect('doctor-list')
        else:
            messages.error(request, "Erreur lors de la modification du mot de passe. Veuillez vérifier les champs.")
        return render(request, 'book/administration/doctor/change-doctor-password.html', {
            'form': form,
            'doctor': doctor,
        })
class DoctorListPlanningView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'book/administration/doctor/doctor-list-planning.html'
    context_object_name = 'doctors'


class DoctorScheduleView(LoginRequiredMixin, View):
    def get(self, request, doctor_id):
        doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
        time_slots = DoctorTimeSlots.objects.filter(doctor=doctor)
        form = DoctorScheduleForm()
        return render(request, 'book/administration/doctor/doctor-schedule.html', {'doctor': doctor, 'time_slots': time_slots, 'form': form})

    def post(self, request, doctor_id):
        doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
        form = DoctorScheduleForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['doc_start_date']
            end_date = form.cleaned_data['doc_end_date']
            time_slot, created = DoctorTimeSlots.objects.get_or_create(
                doctor=doctor,
                doc_start_date=start_date,
                doc_end_date=end_date,
            )
            if created:
                messages.success(request, 'Créneau ajouté avec succès.')
            else:
                messages.warning(request, 'Ce créneau existe déjà.')
        else:
            messages.error(request, 'Une erreur est survenue lors de l\'ajout du créneau.')
        return redirect('doctor-schedule-list')

class DoctorScheduleListView(LoginRequiredMixin, View):
    def get(self, request):
        doctors = Doctor.objects.all().prefetch_related('doctortimeslots_set')
        context = {
            'doctors': doctors
        }
        return render(request, 'book/administration/doctor/doctor-schedule-list.html', context)

class DeleteTimeSlotView(LoginRequiredMixin, View):
    def post(self, request, timeslot_id):
        timeslot = get_object_or_404(DoctorTimeSlots, id=timeslot_id)
        timeslot.delete()
        messages.success(request, "Le créneau a été supprimé avec succès.")
        return redirect('doctor-schedule-list')

class UpdateTimeSlotsView(LoginRequiredMixin, View):
    def post(self, request, time_slot_id):
        try:
            time_slot = DoctorTimeSlots.objects.get(id=time_slot_id)
            start_date = request.POST.get('startDate')
            end_date = request.POST.get('endDate')

            if start_date and end_date:
                time_slot.doc_start_date = date.fromisoformat(start_date)
                time_slot.doc_end_date = date.fromisoformat(end_date)
                time_slot.save()
                messages.success(request, f"Le créneau a été mis à jour avec succès.")
            else:
                messages.error(request, f"Les dates pour le créneau {time_slot_id} sont invalides.")

        except DoctorTimeSlots.DoesNotExist:
            messages.error(request, f"Le créneau avec l'ID {time_slot_id} n'existe pas.")
        except ValueError:
            messages.error(request, f"Les dates pour le créneau {time_slot_id} sont invalides.")

        return redirect('doctor-schedule-list')



class CreateSecretaryView(LoginRequiredMixin, View):
    def get(self, request):
        form = SecretaryForm()
        return render(request, 'book/administration/secretary/create-secretary.html', {'form': form})

    def post(self, request):
        form = SecretaryForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Générer un numéro d'enregistrement unique
                    reg_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                    while Secretary.objects.filter(reg_number=reg_number).exists():
                        reg_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

                    # Créer un nouvel utilisateur
                    user = User.objects.create_user(
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password1']
                    )
                    messages.debug(request, f"Utilisateur créé avec succès : {user}")

                    secretary = form.save(commit=False)
                    secretary.user = user
                    secretary.reg_number = reg_number  # Attribuer le numéro d'enregistrement
                    secretary.save()

                    # Attribuer le rôle 'is_secretary'
                    user.is_secretary = True
                    user.save()

                    secretary_group, created = Group.objects.get_or_create(name='is_secretary')
                    secretary.user.groups.add(secretary_group)

                    messages.success(request, "La secrétaire a été créée avec succès.")
                    return redirect('secretary-list')  # Assurez-vous que 'secretary-list' est défini dans vos URLs
            except IntegrityError as e:
                messages.error(request, f"Une erreur est survenue lors de la création de la secrétaire : {e}")
        else:
            messages.error(request, "Erreur lors de la création de la secrétaire. Veuillez vérifier les champs.")

        return render(request, 'book/administration/secretary/create-secretary.html', {'form': form})
class SecretaryListView(LoginRequiredMixin, ListView):
    model = Secretary
    template_name = 'book/administration/secretary/secretary-list.html'
    context_object_name = 'secretaries'

class EditSecretaryView(LoginRequiredMixin, View):
    def get(self, request, secretary_id):
        secretary = get_object_or_404(Secretary, pk=secretary_id)
        form = EditSecretaryForm(instance=secretary)
        password_form = ChangePasswordForm(secretary.user)
        return render(request, 'book/administration/secretary/edit-secretary.html', {
            'form': form,
            'secretary': secretary,
            'password_form': password_form,
        })

    def post(self, request, secretary_id):
        secretary = get_object_or_404(Secretary, pk=secretary_id)
        form = EditSecretaryForm(request.POST, instance=secretary)

        if form.is_valid():
            secretary = form.save(commit=False)
            user = secretary.user
            user.email = form.cleaned_data['email']
            user.save()
            secretary.save()
            request.session['secretary_updated_success'] = True
            return redirect('secretary-list')
        else:
            messages.error(request, "Erreur de mise à jour des informations. Veuillez vérifier les champs.")
            password_form = ChangePasswordForm(secretary.user)

        return render(request, 'book/administration/secretary/edit-secretary.html', {
            'form': form,
            'secretary': secretary,
            'password_form': password_form,
        })

class DeleteSecretaryView(LoginRequiredMixin, View):
    def post(self, request, pk):
        secretary = get_object_or_404(Secretary, pk=pk)
        secretary_name = f"{secretary.first_name} {secretary.last_name}"
        secretary.delete()
        messages.success(request, f"La secrétaire {secretary_name} a été supprimée avec succès.")
        return redirect('secretary-list')


class ChangeSecretaryPasswordView(LoginRequiredMixin, View):
    def get(self, request, secretary_id):
        secretary = get_object_or_404(Secretary, secretary_id=secretary_id)
        user = secretary.user
        form = ChangePasswordForm(user)
        return render(request, 'book/administration/secretary/change-secretary-password.html', {
            'form': form,
            'secretary': secretary,
        })

    def post(self, request, secretary_id):
        secretary = get_object_or_404(Secretary, secretary_id=secretary_id)
        user = secretary.user
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            request.session['password_changed_success'] = True  # Stocker le message de succès dans la session
            return redirect('secretary-list')
        else:
            messages.error(request, "Erreur lors de la modification du mot de passe. Veuillez vérifier les champs.")
        return render(request, 'book/administration/secretary/change-secretary-password.html', {
            'form': form,
            'secretary': secretary,
        })

