from django.contrib import admin
from . models import (Services, Appointments, DoctorServices, DoctorTimeSlots)

# Register your models here.

# The class specifies how we want our Services data model to be displayed in the Django Admin
class ServicesAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    #This creates a search field on the admin
    search_fields = ('name',)

class DoctorServicesAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'service']

class DoctorTimeSlotsAdmin(admin.ModelAdmin):
    list_display = ['Doctor_Name','Doctor_Service','date', 'start_time', 'end_time']

    # Method to display the doctors Name in the Django admin dashboard.it overrides the __str__ method in the models.py
    def Doctor_Name(self, doctorTimeSlots):
        return doctorTimeSlots.doctor_service.doctor.username
    
    # Method to display the doctors service in the Django admin dashboard.it overrides the __str__ method in the models.py
    def Doctor_Service(self, doctorService):
        return doctorService.doctor_service.service

class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ['patient','Appointment_Date', 'booking_code']

    def Appointment_Date(self, appointments):
        return appointments.doctor_time_slots.date
    

    

admin.site.register(Services, ServicesAdmin)
admin.site.register(Appointments, AppointmentsAdmin)
admin.site.register(DoctorServices, DoctorServicesAdmin)
admin.site.register(DoctorTimeSlots, DoctorTimeSlotsAdmin)
# admin.site.register(Hospitals)

