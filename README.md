# Hospital Appointment Management System
The system interacts with Africa's Talking APIs to enable seamless Hospital Appointment Booking. 
The patient log's into the given hospital's platform and checks the available Doctor Time slots for an appointment, the type of services being offered by that Hospital and the Doctor offering that service.

To book an appointment :
 - The Patient dials a Specified U.S.S.D code e.g (*)384(*)743106(#), 
 - Selects the service he/she requires.
 - Selects the doctor available to offer an appointment for that given service
 - If the given time is convinient to the patient, the patient selects it.
 - Upon successful completion of the above steps, A message is sent back to the patient's phone number which contains the generated Booking Code. 
 - This booking code is used by both the Doctor and the Hospital to verify this Patient's Appointment.
  
# Quick Guide <br />

Below are the steps on how to get the web app up and running

- Clone it: <br />
    git clone https://github.com/john-thuo1/hospitalbookingmanagementsystem.git <br />

- Cd into it: <br />
    cd djangohospitalappointment <br />

- Create a virtual environment
    python3 -m venv venv <br />
     
- Activate venv: <br />
    Mac/Linux: source venv/bin/activate <br />
    Windows: venv\Scripts\activate <br />
    
- Install the requirements <br />
    pip install -r requirements.txt <br />
    
- Create DB <br />
    python manage.py makemigrations <br />
    
- Apply DB Changes <br />
    python manage.py migrate <br />
    
- Create a Ngrok URL: <br />
      Follow this link for more details : https://medium.com/@johnthuo/part-2-integrating-africas-talking-apis-into-the-hospital-management-system-5e7a2cd16345
      Do not close or quit this ngrok shell <br />
 
- Configure your Africa’s Talking U.S.S.D. A.P.I.: <br />
      Follow this link for more details : https://medium.com/@johnthuo/part-2-integrating-africas-talking-apis-into-the-hospital-management-system-5e7a2cd16345
      

- Run the server: <br />
   python manage.py runserver <br />

- Navigate to your localhost site <br />
   Follow the instructions on the home page to start using the site
  
  



