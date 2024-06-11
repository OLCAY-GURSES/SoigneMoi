from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AdminViewSet, HospitalViewSet, SpecializationViewSet, PatientViewSet, DoctorViewSet, \
    DoctorTimeSlotsViewSet, PrescriptionViewSet, PrescriptionMedicineViewSet, \
    PrescriptionTestViewSet, TestInformationViewSet, ObtainAuthTokenView, SecretaryDashboardView, \
    DoctorDashboardView, DoctorViewPrescription, PatientProfileAPIView, \
    CreatePrescriptionView, DoctorUpdateMedicineEndDate

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'admins', AdminViewSet)
#router.register(r'hospitals', HospitalViewSet)
router.register(r'specializations', SpecializationViewSet)
router.register(r'patients', PatientViewSet)
#router.register(r'doctors', DoctorViewSet)
router.register(r'doctor-time-slots', DoctorTimeSlotsViewSet)

router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'prescription-medicines', PrescriptionMedicineViewSet)
router.register(r'prescription-tests', PrescriptionTestViewSet)
router.register(r'test-information', TestInformationViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', ObtainAuthTokenView.as_view(), name='api_token_auth'),
    path('secretary/dashboard/', SecretaryDashboardView.as_view(), name='secretary_dashboard'),
    path('doctor/dashboard/', DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('prescriptions/<int:pk>/', DoctorViewPrescription.as_view(), name='doctor-view-prescription'),
    path('patient/profile/<int:pk>/', PatientProfileAPIView.as_view(), name='patient-profile'),
    path('prescriptions/create/<int:pk>/', CreatePrescriptionView.as_view(), name='create_prescription'),
    path('prescriptions/<int:prescription_id>/medicines/<int:prescription_medicine_id>/end_date/',
         DoctorUpdateMedicineEndDate.as_view(), name='update_medicine_end_date'),
    #path('prescriptions/<int:prescription_id>/medicines/<int:prescription_medicine_id>/end_date/', UpdatePrescriptionMedicineEndDate.as_view(),\
     #name='update-prescription-medicine-end-date'),
    #path('prescriptions/create/<int:pk>/', CreatePrescriptionAPIView.as_view(), name='create-prescription'),


]