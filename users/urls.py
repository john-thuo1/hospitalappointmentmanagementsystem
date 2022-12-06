from django.urls import path,include
from re import template
from django.contrib import admin
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

from users.views import (PatientsListView, PatientsCreateView, PatientsUpdateView, PatientsDeleteView,
                         DoctorsListView, DoctorsCreateView, DoctorsUpdateView, DoctorsDeleteView)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    path('patients', PatientsListView.as_view(), name='patients-list'),
    path('patients/new/', PatientsCreateView.as_view(), name='patients-create'),
    path('patients/<int:pk>/update/', PatientsUpdateView.as_view(), name='patients-update'),
    path('patients/<int:pk>/delete/', PatientsDeleteView.as_view(), name='patients-delete'),
    path('doctors', DoctorsListView.as_view(), name='doctors-list'),
    path('doctors/new/', DoctorsCreateView.as_view(), name='doctors-create'),
    path('doctors/<int:pk>/update/', DoctorsUpdateView.as_view(), name='doctors-update'),
    path('doctors/<int:pk>/delete/', DoctorsDeleteView.as_view(), name='doctors-delete'),
]