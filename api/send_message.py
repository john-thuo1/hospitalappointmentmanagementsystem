import requests


def send(phone_number, message="Hi from Africa's Talking"):
    payload = {
        "username": 'sandbox',
        "to": f"{phone_number}",
        "message": message,
        "from": 74310 # replace this with your short code
    }

    header = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        'apiKey': 'd961d567468beb8b95975eef380ccb70a3b9dce12ret37u3iw7shs8sjs9sjs' # Use your own API KEY.
    }


    req = requests.post('https://api.sandbox.africastalking.com/version1/messaging', data=payload, headers=header)

    req = req.json()
    message_data = req['SMSMessageData']
    status = message_data["Recipients"][0]['status']

    return status
