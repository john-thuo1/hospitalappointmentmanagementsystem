from django.urls import path

from hospital.views import (about, home, ServicesListView, ServicesCreateView, ServicesUpdateView, ServicesDeleteView,
                            DoctorServicesListView, DoctorServicesCreateView, DoctorServicesUpdateView,
                            DoctorServicesDeleteView,
                            DoctorTimeSlotsListView, DoctorTimeSlotsCreateView, DoctorTimeSlotsUpdateView,
                            DoctorTimeSlotsDeleteView,
                            AppointmentsListView, AppointmentsCreateView, AppointmentsUpdateView,
                            AppointmentsDeleteView)

urlpatterns = [
    path('about', about, name='about'),
    path('', home, name='home'),
    path('services', ServicesListView.as_view(), name='services-list'),
    path('services/new/', ServicesCreateView.as_view(), name='services-create'),
    path('services/<int:pk>/update/', ServicesUpdateView.as_view(), name='services-update'),
    path('services/<int:pk>/delete/', ServicesDeleteView.as_view(), name='services-delete'),
    path('doctor_services', DoctorServicesListView.as_view(), name='doctor-services-list'),
    path('doctor_services/new/', DoctorServicesCreateView.as_view(), name='doctor-services-create'),
    path('doctor_services/<int:pk>/update/', DoctorServicesUpdateView.as_view(), name='doctor-services-update'),
    path('doctor_services/<int:pk>/delete/', DoctorServicesDeleteView.as_view(), name='doctor-services-delete'),
    path('doctor_time_slots', DoctorTimeSlotsListView.as_view(), name='doctor-time-slots-list'),
    path('doctor_time_slots/new/', DoctorTimeSlotsCreateView.as_view(), name='doctor-time-slots-create'),
    path('doctor_time_slots/<int:pk>/update/', DoctorTimeSlotsUpdateView.as_view(), name='doctor-time-slots-update'),
    path('doctor_time_slots/<int:pk>/delete/', DoctorTimeSlotsDeleteView.as_view(), name='doctor-time-slots-delete'),
    path('appointments', AppointmentsListView.as_view(), name='appointments-list'),
    path('appointments/new/', AppointmentsCreateView.as_view(), name='appointments-create'),
    path('appointments/<int:pk>/update/', AppointmentsUpdateView.as_view(), name='appointments-update'),
    path('appointments/<int:pk>/delete/', AppointmentsDeleteView.as_view(), name='appointments-delete'),
]