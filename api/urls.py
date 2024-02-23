from django.urls import path, include
from rest_framework import routers
from api.views import LogoutView, LoginView, DoctorDashboardView, DoctorProfileView, CreatePrescriptionView, \
    ViewPrescriptionView, SecretaryViewSet

router = routers.DefaultRouter()
router.register(r'logout', LogoutView, basename='logout')
router.register(r'login', LoginView, basename='login')
router.register(r'doctor_dashboard', DoctorDashboardView, basename='doctor_dashboard')
router.register(r'doctor_profile', DoctorProfileView, basename='doctor_profile')
router.register(r'create_prescription', CreatePrescriptionView, basename='create_prescription')
router.register(r'view_prescription', ViewPrescriptionView, basename='view_prescription')
router.register(r'secretary_dashboard', SecretaryViewSet, basename='secretary_dashboard')
#router.register(r'other', OtherViewSet)

urlpatterns = [
    # Autres URL de votre projet...
    path('', include(router.urls)),
]