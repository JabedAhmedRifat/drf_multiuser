from django.urls import path
from .views import *
from knox import views as knox_views

urlpatterns = [
    path('register/',RegistrationAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
    path('get-user/', UserAPI.as_view()),
    path('change-password/', changePasswordView),
    
    path('reset-password/', ResetPasswordAPI.as_view()),
    path('set-new-password/<str:uid>/<str:token>/', SetNewPasswordAPI.as_view()),
]
