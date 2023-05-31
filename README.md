# Hospital Appointment Management System

The Hospital Appointment Management System is a comprehensive solution that leverages Africa's Talking APIs to facilitate seamless hospital appointment booking. This system allows patients to log into their respective hospital's platform and access information about available doctor time slots, types of services offered, and the doctors providing those services.

## Viewing the Hospital Appointment Management System Dashboard

To access the website dashboard, please refer to the **WebsiteDashboard.md** file. For a detailed view of the mobile user interface screens, please consult the **MobileUIDashboard.md** file.

## Booking an Appointment

The appointment booking process involves the following steps:

1. The patient dials a specified USSD code, such as (*)384(*)743106(#), on their phone.
2. The patient selects the desired service from the available options.
3. The patient selects a doctor who is available to provide an appointment for the chosen service.
4. If the suggested time slot is convenient for the patient, they confirm their selection.
5. Once the above steps are successfully completed, a message containing the generated booking code is sent to the patient's phone number. This code serves as verification for the patient's appointment and is used by both the doctor and the hospital.

## Quick Guide

Follow the steps below to set up and run the web app:

1. Clone the repository:
   ```shell
   git clone https://github.com/john-thuo1/hospitalbookingmanagementsystem.git
   ```

2. Change into the project directory:
   ```shell
   cd djangohospitalappointment
   ```

3. Create a virtual environment:
   ```shell
   python3 -m venv venv
   ```

4. Activate the virtual environment:
   - Windows:
     ```shell
     venv\Scripts\activate
     ```

5. Install the required dependencies:
   ```shell
   pip install -r requirements.txt
   ```

6. Create the database:
   ```shell
   python manage.py makemigrations
   ```

7. Apply database changes:
   ```shell
   python manage.py migrate
   ```

8. Create a Ngrok URL:
   Please refer to this link for detailed instructions: [Integrating Africa's Talking APIs into the Hospital Management System](https://medium.com/@johnthuo/part-2-integrating-africas-talking-apis-into-the-hospital-management-system-5e7a2cd16345)
   Ensure that you do not close or quit the Ngrok shell during this process.

9. Configure your Africa's Talking USSD API:
   Please follow this link for detailed instructions: [Integrating Africa's Talking APIs into the Hospital Management System](https://medium.com/@johnthuo/part-2-integrating-africas-talking-apis-into-the-hospital-management-system-5e7a2cd16345)

10. Start the server:
    ```shell
    python manage.py runserver <port_number>
    ```
    For example:
    ```shell
    python manage.py runserver 3000
    ```

11. Access the site on your localhost:
    Follow the instructions provided on the home page to begin using the site.
