from rest_framework.response import Response
from rest_framework.decorators import api_view
from hospital.models import DoctorServices, DoctorTimeSlots, Services, Appointments
from users.models import Patients, Doctors
from  api.generate_code import get_code
import api.send_message as send_message



# Function returns a list of Hospital Services being offered.
def get_service_object(index=None):
    service = Services.objects.values_list('id', 'name')
    if index is None:
        return service
    else:
        if 0 < index <= len(service):
            return service[index - 1]
        else:
            return None


# Function returns a list of doctors/single doctor that offers a given hospital service.
def get_doctor_services_object(service_id, index=None):
    doctor_service = DoctorServices.objects.filter(
        service_id=service_id).values_list('pk', 'doctor__first_name', 'doctor__last_name')
    if index is None:
        # returns a QuerySet e.g. [(1, 'Meak' 'Row')]
        return doctor_service
    else:
        if 0 < index <= len(doctor_service):
            return doctor_service[index - 1]
        else:
            return None


# Function returns a list of available dates a given Doctor can take an appointment
def get_doctor_time_slot_object(doctor_service_id, index=None):
    doctor_time_slots = DoctorTimeSlots.objects.filter(
        doctor_service_id=doctor_service_id).values_list('pk', 'start_date', 'end_date')
    if index is None:
        # returns a QuerySet e.g. [(1, 'start_date', 'end_date')]
        return doctor_time_slots
    else:
        if len(doctor_time_slots) > 0:
            # returns a single tuple with the service id and name e.g.(1, 'Meak', 'Row')
            return doctor_time_slots[index - 1]
        else:
            return None


# Function generates services that will be displayed to a user
def get_services():
    # This is the index that will be displayed to the user for selection
    count = 0
    response = "CON Select Service \n"
    for index, service in get_service_object():
        count += 1
        response += f"{count}. {service} \n"
    return response


# Function generates a list of doctors that offer the service that the user selected
def get_doctor_services(service_id):
    # This is the index that will be displayed to the user for selection
    count = 0
    doctor_services_object = get_doctor_services_object(service_id=service_id)

    if doctor_services_object is None:
        return "END No Doctor Available for the Service \n"

    response = "CON Select Doctor \n"
    for index, doctor__first_name, doctor__last_name in doctor_services_object:
        count += 1
        response += f"{count}. {doctor__first_name} {doctor__last_name} \n"

    if count == 0:
        response = "END No Doctor Available for the Service \n"

    return response


# Function generates a list of dates the selected doctor that offers the selected service will be available for consultation.

def get_doctor_time_slot(doctor_service_id):
    # This is the index that will be displayed to the user for selection
    count = 0
    doctor_time_slot_object = get_doctor_time_slot_object(doctor_service_id=doctor_service_id)

    if doctor_time_slot_object is None:
        return "END No Appointments Available Yet \n"

    response = "CON Select Slot to Book\n"
    for index, start_date, end_date in doctor_time_slot_object:
        count += 1
        response += f"{count}. {start_date} \n"

    if count == 0:
        response = "END No Appointments Available Yet \n"
    return response


@api_view(['GET', 'POST'])
def ussd_callback(request):
    response = ""
    request = request.data
    session_id = request.get("sessionId", None)
    service_code = request.get("serviceCode", None)
    phone_number = request.get("phoneNumber", None)
    text = request.get("text", "default")

    # The first call of the U.S.S.D. will send a blank text to the view, this will prompt us to first
    # display the services available
    if text == '':
        response = get_services()
    else:
      
        values = text.split("*")
        if len(values) == 1:
            selected_service_index = int(values[0])
          .
            selected_service = get_service_object(selected_service_index)
            selected_service_id = -1
            if selected_service is not None:
                selected_service_id = selected_service[0]

        
            response = get_doctor_services(selected_service_id)
        elif len(values) == 2:
            selected_service_index = int(values[0])
           
            selected_service = get_service_object(selected_service_index)
            selected_service_id = selected_service[0]

            selected_doctor_index = int(values[1])
          
            selected_doctor_service = get_doctor_services_object(service_id=selected_service_id,
                                                                 index=selected_doctor_index)

            selected_doctor_service_id = -1
            if selected_doctor_service is not None:
            
                selected_doctor_service_id = selected_doctor_service[0]

  
            response = get_doctor_time_slot(selected_doctor_service_id)
        elif len(values) == 3:
            selected_service_index = int(values[0])
           
            selected_service = get_service_object(selected_service_index)
            selected_service_id = selected_service[0]

            # get the index of the doctor that was selected
            selected_doctor_index = int(values[1])
         
            selected_doctor_service = get_doctor_services_object(service_id=selected_service_id,
                                                                 index=selected_doctor_index)

            selected_doctor_service_id = selected_doctor_service[0]

            selected_doctor_time_slot_index = int(values[2])
      
            selected_doctor_time_slot = get_doctor_time_slot_object(selected_doctor_service_id,
                                                                    index=selected_doctor_time_slot_index)
            selected_doctor_time_slot_id = selected_doctor_time_slot[0]

            doctor_time_slot = DoctorTimeSlots.objects.get(pk=selected_doctor_time_slot_id)
            patient = Patients.objects.filter(phone_number=phone_number)
            booking_code = get_code()

            if len(patient) > 0:
                appointment = Appointments.objects.create(doctor_time_slots=doctor_time_slot, patient=patient.first(), booking_code = booking_code)

                if appointment is None:
                    response = "END Appointment Failed"
                else:
                    response = "END Your Appoinment has been booked!"
                    send_message.send(phone_number, f"Appointment Booked Successfully. Your booking code is {booking_code}")
            else:
                response = "END You Are Not a Registered Patient"


    return Response(response, headers={"Content-Type": "text/plain"})
