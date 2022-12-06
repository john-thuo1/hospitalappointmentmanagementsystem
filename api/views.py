from rest_framework.response import Response
from rest_framework.decorators import api_view
from hospital.models import DoctorServices, DoctorTimeSlots, Services, Appointments
from users.models import Patients
from  api.generate_code import get_code
import api.send_message as send_message



def get_service_object(index=None):
    service = Services.objects.values_list('id', 'name')
    if index is None:
        return service
    else:
        if 0 < index <= len(service):
            return service[index - 1]
        else:
            return None


def get_doctor_services_object(service_id, index=None):
    doctor_service = DoctorServices.objects.filter(
        service_id=service_id).values_list('pk', 'doctor__first_name', 'doctor__last_name')
    if index is None:
        return doctor_service
    else:
        if 0 < index <= len(doctor_service):
            return doctor_service[index - 1]
        else:
            return None

def get_doctor_time_slot_object(doctor_service_id, index=None):
    doctor_time_slots = DoctorTimeSlots.objects.filter(
        doctor_service_id=doctor_service_id).values_list('pk', 'date', 'start_time', 'end_time')
    if index is None:
        return doctor_time_slots
    else:
        if len(doctor_time_slots) > 0:
            return doctor_time_slots[index - 1]
        else:
            return None


# A function used to generate services that will be displayed to a user
def get_services():
    count = 0
    response = "CON Select Service \n"
    for index, service in get_service_object():
        count += 1
        response += f"{count}. {service} \n"
    return response


# The function used to generate a list of doctors that offer the service that the user selected
def get_doctor_services(service_id):
    count = 0
    doctor_services_object = get_doctor_services_object(service_id=service_id)

    if doctor_services_object is None:
        return "END No Doctor Available for the Service \n"

    response = "CON Select Doctor \n"
    for index, doctor__first_name, doctor__last_name in doctor_services_object:
        count += 1
        response += f"{count}. Dr {doctor__first_name} {doctor__last_name} \n"

    if count == 0:
        response = "END No Doctor Available for the Service \n"

    return response



def get_doctor_time_slot(doctor_service_id):
    count = 0
    doctor_time_slot_object = get_doctor_time_slot_object(doctor_service_id=doctor_service_id)

    if doctor_time_slot_object is None:
        return "END No Appointments Available Yet \n"

    response = "CON Select Slot to Book\n"
    for index, date, start_time, end_time in doctor_time_slot_object:
        count += 1
        response += f"{count}. {date} from {start_time} to {end_time}\n"

    if count == 0:
        response = "END No Appointments Available Yet \n"
  
        
    return response


# The view that the U.S.S.D. will use to display data to the user
@api_view(['GET', 'POST'])
def ussd_callback(request):
    response = ""
    request = request.data
    session_id = request.get("sessionId", None)
    service_code = request.get("serviceCode", None)
    phone_number = request.get("phoneNumber", None)
    text = request.get("text", "default")
    if text == '':
        response = get_services()
    else:

        values = text.split("*")

        if len(values) == 1:
            selected_hospital_index = int(values[0])

            selected_service_index = int(values[0])

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

            selected_doctor_index = int(values[1])

            selected_doctor_service = get_doctor_services_object(service_id=selected_service_id,index=selected_doctor_index)

            selected_doctor_service_id = selected_doctor_service[0]

            selected_doctor_time_slot_index = int(values[2])

            selected_doctor_time_slot = get_doctor_time_slot_object(selected_doctor_service_id, index=selected_doctor_time_slot_index)

            selected_doctor_time_slot_id = selected_doctor_time_slot[0]

            doctor_time_slot = DoctorTimeSlots.objects.get(pk=selected_doctor_time_slot_id)
            patient = Patients.objects.filter(phone_number=phone_number)
            booking_code = get_code()

            if len(patient) > 0:
                appointment = Appointments.objects.create(doctor_time_slots=doctor_time_slot, patient=patient.first(),booking_code=booking_code)

                if appointment is None:
                    response = "END Appointment Failed"
                else:

                    response = "END Appointment Booked Successfully. Confirmation message will be sent to you shortly!"
                    send_message.send(phone_number, f"Dear {appointment.patient},\n"
                                      f"Your Appointment with Dr {doctor_time_slot.doctor_service.doctor.first_name} {doctor_time_slot.doctor_service.doctor.last_name} of \n"
                                      f"{doctor_time_slot.doctor_service.service} services has been Booked Successfully.\n"
                                      f"Your booking code is {booking_code} and the appointment date is on {appointment.doctor_time_slots.date} at {appointment.doctor_time_slots.start_time}.\n" 
                                      f" Please avail your booking code when visiting the Hospital!\n"
                                      f" If you need to, Please login to our hospital site to upload your recent medical records!"
                                      f" Thank you!")

            else:
                response = "END You Are Not a Registered Patient."

    return Response(response, headers={"Content-Type": "text/plain"})
