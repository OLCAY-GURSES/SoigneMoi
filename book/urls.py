from django.urls import path
from .views import (
    HomeView, ListHospitalView, LogoutView, LoginView, PatientRegisterView,
    PatientDashboardView, ProfileSettingsView, ChangePasswordView, SearchView,
    BookingView, PrescriptionView, AdminDashboardView, HospitalCreateView, HospitalListView, HospitalUpdateView,
    HospitalDeleteView, SpecializationDeleteView, CreateDoctorView, DoctorListView, EditDoctorView,
    ChangeDoctorPasswordView, DeleteDoctorView, DoctorListPlanningView, DoctorScheduleView, DoctorScheduleListView,
    DeleteTimeSlotView, UpdateTimeSlotsView, CreateSecretaryView, SecretaryListView, EditSecretaryView,
    DeleteSecretaryView, ChangeSecretaryPasswordView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='hospital_home'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    ######PATIENT######
    path('patient-register/', PatientRegisterView.as_view(), name='patient-register'),
    path('change-password/<int:pk>/', ChangePasswordView.as_view(), name='change-password'),
    path('patient-dashboard/', PatientDashboardView.as_view(), name='patient-dashboard'),
    path('profile-settings/', ProfileSettingsView.as_view(), name='profile-settings'),
    path('list-hospital/', ListHospitalView.as_view(), name='list-hospital'),
    path('search/', SearchView.as_view(), name='search'),
    path('booking/<int:pk>/', BookingView.as_view(), name='booking'),
    path('prescription-view/<int:pk>', PrescriptionView.as_view(), name='prescription-view'),

    ######ADMIN######
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),

    ######ADMIN/HOSPITAL######
    path('hospital/add/', HospitalCreateView.as_view(), name='add-hospital'),
    path('hospital/list/', HospitalListView.as_view(), name='hospital-list'),
    path('hospital/edit/<int:pk>/', HospitalUpdateView.as_view(), name='edit-hospital'),
    path('hospital/delete/<int:pk>/', HospitalDeleteView.as_view(), name='delete-hospital'),
    path('specialization/delete/<int:pk>/<int:pk2>/', SpecializationDeleteView.as_view(), name='delete-specialization'),

    ######ADMIN/DOCTOR######

    path('create_doctor/',CreateDoctorView.as_view(), name='create_doctor'),
    path('doctor-list/', DoctorListView.as_view(), name='doctor-list'),
    path('edit-doctor/<int:doctor_id>/', EditDoctorView.as_view(), name='edit-doctor'),
    path('doctors/<int:doctor_id>/change-password/', ChangeDoctorPasswordView.as_view(), name='change-doctor-password'),
    path('delete-doctor/<int:pk>/', DeleteDoctorView.as_view(), name='delete-doctor'),
    path('doctor-list-planning/', DoctorListPlanningView.as_view(), name='doctor-list-planning'),
    path('doctor/<int:doctor_id>/schedule/', DoctorScheduleView.as_view(), name='doctor-schedule'),
    path('doctor-schedule/', DoctorScheduleListView.as_view(), name='doctor-schedule-list'),
    path('delete-timeslot/<int:timeslot_id>/', DeleteTimeSlotView.as_view(), name='delete-timeslot'),
    path('update-time-slots/<int:time_slot_id>/', UpdateTimeSlotsView.as_view(), name='update-time-slots'),



    ######ADMIN/SECRETARY######
    path('create-secretary/', CreateSecretaryView.as_view(), name='create-secretary'),
    path('secretaries/', SecretaryListView.as_view(), name='secretary-list'),
    path('edit-secretary/<int:secretary_id>/', EditSecretaryView.as_view(), name='edit-secretary'),
    path('delete-secretary/<int:pk>/', DeleteSecretaryView.as_view(), name='delete-secretary'),
    path('secretaires/<int:secretary_id>/changer-mot-de-passe/', ChangeSecretaryPasswordView.as_view(), name='change-secretary-password'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
