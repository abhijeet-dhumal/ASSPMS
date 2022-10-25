from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from account import fe_views
from account.views import (
    RegisterView,
    MyObtainTokenPairView,
    Profile,
    RequestUpdateProfileView,
    Snippet,
    RequestPasswordResetEmail,
    SetNewPasswordAPIView,
    PasswordTokenCheckAPI,
    APIChangePasswordView
)


urlpatterns = [
     path('', fe_views.home,name="home"),
     path('login/', fe_views.LoginForm,name="LoginForm"),
     path('register/', fe_views.RegisterForm,name="RegisterForm"),
     path('dashboard/',fe_views.dashboard,name="dashboard"),
     path('userdetails/<str:pk>/', fe_views.userdetails,name="userdetails"),
     path('logout/', fe_views.logoutuser, name ='logoutuser'),

     # REST FRAMEWORK URLS
     path('api_register', RegisterView.as_view(), name='auth_register'),
     path('api_login', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
     path('api_login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
     path('api_profile', Profile.as_view(), name='profile'),
     path('api_snippet', Snippet.as_view(), name='snippet'),

     # forgot password
     path('api_request-password-reset-email/', RequestPasswordResetEmail.as_view(),
          name="request-password-reset-email"),
     path('api_password-reset/<uidb64>/<token>/',
          PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
     path('api_password-reset-complete', SetNewPasswordAPIView.as_view(),
          name='password-reset-complete'),

     # reset password after login
     path('api_change-password', APIChangePasswordView.as_view(),
          name='change-password'),

     path('api_request-update-profile/<int:pk>', RequestUpdateProfileView.as_view(),
          name='request-update-profile')
]
