# perdiems/urls.py
from django.urls import path
from . import views
from .views import CustomLoginApiView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login_view'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout_view' ),

    # llamado a jason webttoken
    path('api/login/', CustomLoginApiView.as_view(), name='login_api'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
