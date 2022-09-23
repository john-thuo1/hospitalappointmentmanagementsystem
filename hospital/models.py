from tabnanny import verbose
from tkinter import CASCADE
from django.db import models
from users.models import (Patients, Doctors)
from django.utils import timezone

# Create your models here.
# Surgery,General Practice, Pulmonology, Dermatology services,Rheumatology services,Orthopaedic Services

class Services(models.Model):
    name = models.CharField(max_length=100)
    # Column holds a brief description of the service
    description =models.TextField(max_length=500, help_text="Provide a description of the Service")

    #Method returns a string representation of the name of the service being provided by the hospital
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Services"
    


# Table holds the services that each doctor offers in the hospital
class DoctorServices(models.Model):
    # on_delete = models.PROTECT
    service = models.ForeignKey(Services, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctors, on_delete=models.PROTECT)
  # Instead of using username , do self.doctor.get_full_name()
    def __str__(self):
        return f"{self.doctor.username} : {self.service.name}"
        
    class Meta:
        verbose_name_plural = "DoctorServices"  
        

    

class DoctorTimeSlots(models.Model):
    # ForeignKey/ManyToMany
    doctor_service = models.ForeignKey(DoctorServices, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    '''
    This is a method in the class “DoctorTimeSlots” class we will create that will be 
    responsible for returning back the string representation of objects or table records created 
    in the “DoctorTimeSlots” table. The string representation method will return is 
    the full name of the doctor, date of the time slot and the time allocation of the slot.'''

    def __str__(self):
        # doctor.get_full_name()
        return f"{self.doctor_service.doctor.username}.  Consulting Date:{self.date} from {self.start_time} to {self.end_time}"
    
    class Meta:
        verbose_name_plural = "DoctorTimeSlots"  

# the table holds time slots each doctor has designated 
# To provide consultation for a particular services they offer
class Appointments(models.Model):
    # 
    doctor_time_slots = models.ForeignKey(DoctorTimeSlots, null=True, on_delete=models.CASCADE)
    patient = models.OneToOneField(Patients, null=True, on_delete=models.PROTECT)
    booking_code = models.CharField(null=True, max_length=6)


    def __str__(self):
        return f"{self.patient.username} booked an appointment on {self.doctor_time_slots.date} from {self.doctor_time_slots.start_time} to {self.doctor_time_slots.end_time}"
    
    class Meta:
        verbose_name_plural = "Appointments"

