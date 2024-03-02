from django.urls import path

from . import views
from .views import UserTokenObtainPairView, UserTokenRefreshView, UserCreateView, UserLoginView, UserViewSet, SecretaryDashboardAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('token/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', UserTokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', UserCreateView.as_view(), name='user_create'),
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    #path('user/logout/', views.logout_view, name='logout'),
    path('secretary/dashboard/', SecretaryDashboardAPIView.as_view(), name='secretary_dashboard'),
]

urlpatterns += router.urls