from django.urls import path
from . import views

urlpatterns = [
    path("superuser_signup/", views.CreateSuperUser.as_view()),
    path("manager_signup/", views.CreateManager.as_view()),
    path("employee_register/", views.CreateEmployee.as_view()),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('changepassword/', views.ChangedPassword.as_view(), name='password'),
    path('ForgotPassword/', views.ForgotPassword.as_view(), name='Forgotpassword'),
    path('ResetPassword/<uid>/<token>/',
         views.ResetPassword.as_view(), name='ResetPassword'),
]
