from django.test import SimpleTestCase
from django.urls import reverse, resolve
from book.views import (
    HomeView, ListHospitalView, LogoutView, LoginView, PatientRegisterView,
    PatientDashboardView, ProfileSettingsView, ChangePasswordView, SearchView,
    BookingView, PrescriptionView, AdminDashboardView, HospitalCreateView, HospitalListView, HospitalUpdateView,
    HospitalDeleteView, SpecializationDeleteView, CreateDoctorView, DoctorListView, EditDoctorView,
    ChangeDoctorPasswordView, DeleteDoctorView, DoctorListPlanningView, DoctorScheduleView, DoctorScheduleListView,
    DeleteTimeSlotView, UpdateTimeSlotsView, CreateSecretaryView, SecretaryListView, EditSecretaryView,
    DeleteSecretaryView, ChangeSecretaryPasswordView
)

class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('hospital_home')
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_patient_register_url_resolves(self):
        url = reverse('patient-register')
        self.assertEqual(resolve(url).func.view_class, PatientRegisterView)

    def test_change_password_url_resolves(self):
        url = reverse('change-password', args=[1])
        self.assertEqual(resolve(url).func.view_class, ChangePasswordView)

    def test_patient_dashboard_url_resolves(self):
        url = reverse('patient-dashboard')
        self.assertEqual(resolve(url).func.view_class, PatientDashboardView)

    def test_profile_settings_url_resolves(self):
        url = reverse('profile-settings')
        self.assertEqual(resolve(url).func.view_class, ProfileSettingsView)

    def test_list_hospital_url_resolves(self):
        url = reverse('list-hospital')
        self.assertEqual(resolve(url).func.view_class, ListHospitalView)

    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func.view_class, SearchView)

    def test_booking_url_resolves(self):
        url = reverse('booking', args=[1])
        self.assertEqual(resolve(url).func.view_class, BookingView)

    def test_prescription_view_url_resolves(self):
        url = reverse('prescription-view', args=[1])
        self.assertEqual(resolve(url).func.view_class, PrescriptionView)

    def test_admin_dashboard_url_resolves(self):
        url = reverse('admin-dashboard')
        self.assertEqual(resolve(url).func.view_class, AdminDashboardView)

    def test_add_hospital_url_resolves(self):
        url = reverse('add-hospital')
        self.assertEqual(resolve(url).func.view_class, HospitalCreateView)

    def test_hospital_list_url_resolves(self):
        url = reverse('hospital-list')
        self.assertEqual(resolve(url).func.view_class, HospitalListView)

    def test_edit_hospital_url_resolves(self):
        url = reverse('edit-hospital', args=[1])
        self.assertEqual(resolve(url).func.view_class, HospitalUpdateView)

    def test_delete_hospital_url_resolves(self):
        url = reverse('delete-hospital', args=[1])
        self.assertEqual(resolve(url).func.view_class, HospitalDeleteView)

    def test_delete_specialization_url_resolves(self):
        url = reverse('delete-specialization', args=[1, 2])
        self.assertEqual(resolve(url).func.view_class, SpecializationDeleteView)

    def test_create_doctor_url_resolves(self):
        url = reverse('create_doctor')
        self.assertEqual(resolve(url).func.view_class, CreateDoctorView)

    def test_doctor_list_url_resolves(self):
        url = reverse('doctor-list')
        self.assertEqual(resolve(url).func.view_class, DoctorListView)

    def test_edit_doctor_url_resolves(self):
        url = reverse('edit-doctor', args=[1])
        self.assertEqual(resolve(url).func.view_class, EditDoctorView)

    def test_change_doctor_password_url_resolves(self):
        url = reverse('change-doctor-password', args=[1])
        self.assertEqual(resolve(url).func.view_class, ChangeDoctorPasswordView)

    def test_delete_doctor_url_resolves(self):
        url = reverse('delete-doctor', args=[1])
        self.assertEqual(resolve(url).func.view_class, DeleteDoctorView)

    def test_doctor_list_planning_url_resolves(self):
        url = reverse('doctor-list-planning')
        self.assertEqual(resolve(url).func.view_class, DoctorListPlanningView)

    def test_doctor_schedule_url_resolves(self):
        url = reverse('doctor-schedule', args=[1])
        self.assertEqual(resolve(url).func.view_class, DoctorScheduleView)

    def test_doctor_schedule_list_url_resolves(self):
        url = reverse('doctor-schedule-list')
        self.assertEqual(resolve(url).func.view_class, DoctorScheduleListView)

    def test_delete_timeslot_url_resolves(self):
        url = reverse('delete-timeslot', args=[1])
        self.assertEqual(resolve(url).func.view_class, DeleteTimeSlotView)

    def test_update_time_slots_url_resolves(self):
        url = reverse('update-time-slots', args=[1])
        self.assertEqual(resolve(url).func.view_class, UpdateTimeSlotsView)

    def test_create_secretary_url_resolves(self):
        url = reverse('create-secretary')
        self.assertEqual(resolve(url).func.view_class, CreateSecretaryView)

    def test_secretary_list_url_resolves(self):
        url = reverse('secretary-list')
        self.assertEqual(resolve(url).func.view_class, SecretaryListView)

    def test_edit_secretary_url_resolves(self):
        url = reverse('edit-secretary', args=[1])
        self.assertEqual(resolve(url).func.view_class, EditSecretaryView)

    def test_delete_secretary_url_resolves(self):
        url = reverse('delete-secretary', args=[1])
        self.assertEqual(resolve(url).func.view_class, DeleteSecretaryView)

    def test_change_secretary_password_url_resolves(self):
        url = reverse('change-secretary-password', args=[1])
        self.assertEqual(resolve(url).func.view_class, ChangeSecretaryPasswordView)