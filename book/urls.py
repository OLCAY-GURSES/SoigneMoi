from django.urls import path
from .views import (
    HomeView, ListHospitalView, LogoutView, LoginView, PatientRegisterView,
    PatientDashboardView, ProfileSettingsView, ChangePasswordView, SearchView,
    BookingView, PrescriptionView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='hospital_home'),
    path('patient-register/', PatientRegisterView.as_view(), name='patient-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/<int:pk>/', ChangePasswordView.as_view(), name='change-password'),
    path('patient-dashboard/', PatientDashboardView.as_view(), name='patient-dashboard'),
    path('profile-settings/', ProfileSettingsView.as_view(), name='profile-settings'),
    path('list-hospital/', ListHospitalView.as_view(), name='list-hospital'),
    path('search/', SearchView.as_view(), name='search'),
    path('booking/<int:pk>/', BookingView.as_view(), name='booking'),
    path('prescription-view/<int:pk>', PrescriptionView.as_view(), name='prescription-view'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
