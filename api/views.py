from rest_framework.response import Response
from rest_framework.decorators import api_view
from hospital.models import DoctorServices, DoctorTimeSlots, Services, Appointments
from users.models import Patients, Doctors
from  api.generate_code import get_code
import api.send_message as send_message



# This method will be used to return either a list of services offered or a single service offered
# by passing an index that will be used to get the specific service from the list of services
# This index passed is the index a user selects, when prompted to choose the service they want
def get_service_object(index=None):
    service = Services.objects.values_list('id', 'name')
    if index is None:
        # returns a QuerySet e.g. [(1, 'Oncology'), (2, 'Orthopedic'), (3, 'Dentistry')]
        return service
    else:
        if 0 < index <= len(service):
            # returns a single tuple with the service id and name e.g.(1, 'Oncology')
            return service[index - 1]
        else:
            return None


# This method will be used to return either a list of doctors that offer a specific service offered
# or a single doctor that offers the specified service.
# By passing an index a user will be get the specific doctor that offers the service from the list
# of doctors that offer the specified service.
# This index passed is the index a user selects, when prompted to choose the doctor they want to see
# This service_is is the id of the service they earlier selected
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


# This method will be used to return either a list of dates the doctor has slotted for consultation bookings
# or a single date the doctor has slotted for consultation booking.
# By passing an index a user will be get the specific date the doctor has slotted for consultation booking from the list
# of dates the doctor has slotted for consultation bookings.
# This index passed is the index a user selects, when prompted to choose the of date they want to book an appointment
# This doctor_service_id is the id of the service they earlier selected that is offered by a specific doctor that they
# had selected.
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


# A method used to generate services that will be displayed to a user
def get_services():
    # This is the index that will be displayed to the user for selection
    count = 0
    response = "CON Select Service \n"
    for index, service in get_service_object():
        count += 1
        response += f"{count}. {service} \n"
    return response


# The method used to generate a list of doctors that offer the service that the user selected
# You pass a service_id that will be used to get doctors offering the specific service
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


# The method used to generate a list of dates the selected doctor that offers the selected service
# will be available for consultation.
# You pass a doctor_service_id that will be used to get dates the selected doctor will offer the
# specific service, from the time slot table.
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


# The view that the U.S.S.D. will use to display data to the user
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
        # All other calls after the first service will not have an empty text, the text will state the index selected
        # during a particular stage or the index selected in the current stage after another index was selected from
        # a previous stage. e.g First Stage a user selects a service, the text returned will be 1, indicating that
        # the selected the first service that was displayed The Second Stage a user selects a doctor,
        # the text returned will be 1*2, indicating that the selected the second doctor that was displayed after they
        # selected the first service that was displayed

        # We are splitting the text so that we see if the user is selecting for the first time or they are selecting
        # again
        values = text.split("*")

        # If the user called the U.S.S.D. for the first time
        if len(values) == 1:
            # get the index of the service that was selected
            selected_service_index = int(values[0])
            # use this index to get the details of the service that was actually selected or return None if a user
            # entered an index that was not displayed or does not exist.
            selected_service = get_service_object(selected_service_index)
            selected_service_id = -1
            if selected_service is not None:
                # The service returned will be a tuple with the id of the service as the first element of the tuple
                selected_service_id = selected_service[0]

            # use the service id get the doctor that performs the specified service, or return an error response if
            # the service selected has no doctor linked to it.
            response = get_doctor_services(selected_service_id)
        # If the user calls the U.S.S.D. for the second time and selects a doctor
        # The text split will have 2 values, one for the index of the selected service and the
        # other for the index of the selected doctor
        elif len(values) == 2:
            # get the index of the service that was selected
            selected_service_index = int(values[0])
            # use this index to get the details of the service that was actually selected or return None if a user
            # entered an index that was not displayed or a service that  does not exist.
            selected_service = get_service_object(selected_service_index)
            # The service returned will be a tuple with the id of the service as the first element of the tuple
            selected_service_id = selected_service[0]

            # get the index of the doctor that was selected
            selected_doctor_index = int(values[1])
            # use this index and service id to get the details of the doctor's service that was actually selected or
            # return None if a user entered an index that was not displayed or a doctor's service index that does not
            # exist.
            selected_doctor_service = get_doctor_services_object(service_id=selected_service_id,
                                                                 index=selected_doctor_index)

            selected_doctor_service_id = -1
            if selected_doctor_service is not None:
                # The doctor service returned will be a tuple with the id of the doctor's service as the first
                # element of the tuple
                selected_doctor_service_id = selected_doctor_service[0]

            # using the doctor service id to get the time slot scheduled by the doctor, or return an error
            # response if the service offered by the  selected doctor has no time slot scheduled.
            response = get_doctor_time_slot(selected_doctor_service_id)
        elif len(values) == 3:
            # get the index of the service that was selected
            selected_service_index = int(values[0])
            # use this index to get the details of the service that was actually selected or return None if a user
            # entered an index that was not displayed or does not exist.
            selected_service = get_service_object(selected_service_index)
            # The service returned will be a tuple with the id of the service as the first element of the tuple
            selected_service_id = selected_service[0]

            # get the index of the doctor that was selected
            selected_doctor_index = int(values[1])
            # use this index to get the details of the doctor that was actually selected or return None if a user
            # entered an index that was not displayed or a doctor that does not exist.
            selected_doctor_service = get_doctor_services_object(service_id=selected_service_id,
                                                                 index=selected_doctor_index)
            # The doctor service returned will be a tuple with the id of the doctor's service as the first
            # element of the tuple
            selected_doctor_service_id = selected_doctor_service[0]

            # get the index of the time slot scheduled by the selected doctor for the selected service
            selected_doctor_time_slot_index = int(values[2])
            # use this index and doctor service id to get the details of the time slot scheduled or return None if a
            # user entered an index that was not displayed or a time slot scheduled index that does not exist.
            selected_doctor_time_slot = get_doctor_time_slot_object(selected_doctor_service_id,
                                                                    index=selected_doctor_time_slot_index)
            # The time slot scheduled returned will be a tuple with the id of the time slot scheduled as the first
            # element of the tuple
            selected_doctor_time_slot_id = selected_doctor_time_slot[0]

            # use the time slot scheduled id get the specified time slot scheduled object
            doctor_time_slot = DoctorTimeSlots.objects.get(pk=selected_doctor_time_slot_id)
            # use the user's phone number to get the patient's details
            patient = Patients.objects.filter(phone_number=phone_number)
            booking_code = get_code()

            # check if a user using the U.S.S.D. is a patient at the hospital
            if len(patient) > 0:
                appointment = Appointments.objects.create(doctor_time_slots=doctor_time_slot, patient=patient.first(), booking_code = booking_code)

                if appointment is None:
                    response = "END Appointment Failed"
                else:
                    response = "END Your Appoinment has been booked!"
                    send_message.send(phone_number, f"Appointment Booked Successfully. Your booking code is {booking_code}")

            # if not alert use they are not registered, you can also choose to extend the functionality of the
            # U.S.S.D. to register the user as a patient and book an appointment for them. For now we will choose
            # former and end the session
            else:
                response = "END You Are Not a Registered Patient"


    return Response(response, headers={"Content-Type": "text/plain"})
