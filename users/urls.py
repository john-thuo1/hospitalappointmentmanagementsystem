from django.urls import path

from users.views import (PatientsListView, PatientsCreateView, PatientsUpdateView, PatientsDeleteView,
                         DoctorsListView, DoctorsCreateView, DoctorsUpdateView, DoctorsDeleteView)

urlpatterns = [
    path('patients', PatientsListView.as_view(), name='patients-list'),
    path('patients/new/', PatientsCreateView.as_view(), name='patients-create'),
    path('patients/<int:pk>/update/', PatientsUpdateView.as_view(), name='patients-update'),
    path('patients/<int:pk>/delete/', PatientsDeleteView.as_view(), name='patients-delete'),
    path('doctors', DoctorsListView.as_view(), name='doctors-list'),
    path('doctors/new/', DoctorsCreateView.as_view(), name='doctors-create'),
    path('doctors/<int:pk>/update/', DoctorsUpdateView.as_view(), name='doctors-update'),
    path('doctors/<int:pk>/delete/', DoctorsDeleteView.as_view(), name='doctors-delete'),
]