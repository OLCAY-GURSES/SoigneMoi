from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', views.home, name='hospital_home'),

    path('patient-register/', views.patient_register, name='patient-register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('change-password/<int:pk>', views.change_password, name='change-password'),
    path('patient-dashboard/', views.patient_dashboard, name='patient-dashboard'),
    path('profile-settings/', views.profile_settings, name='profile-settings'),

    path('doctor-dashboard/', views.doctor_dashboard, name='doctor-dashboard'),
    path('doctor-profile-settings/', views.doctor_profile_settings, name='doctor-profile-settings'),

    path('list-hospital/', views.list_hospital, name='list-hospital'),
    path('search/', views.search, name='search'),

    path('booking/<int:pk>/', views.booking, name='booking'),

    path('patient-profile/<int:pk>/', views.patient_profile, name='patient-profile'),
    path('create-prescription/<int:pk>/', views.create_prescription, name='create-prescription'),
    path('doctor-view-prescription/<int:pk>/', views.doctor_view_prescription, name='doctor-view-prescription'),
    path('prescription-view/<int:pk>', views.prescription_view, name='prescription-view'),

    # URL pour afficher la liste des secrétaires
    #path('secretaries/', views.secretary_dashboard, name='secretary_list'),




]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
