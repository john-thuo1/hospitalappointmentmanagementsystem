import requests


def send(phone_number, message="Hi from Africa's Talking"):
    payload = {
        "username": 'sandbox',
        "to": f"{phone_number}",
        "message": message,
        "from": 53624  # Create a short Code using SMS Africa's Talking API
        # Channel Created is *384*536247#
    }

    header = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        'apiKey': '19df4062c0da8e304bddac3ed7b7f2610c67f9281e7c1184b004c0bb7a47ff08'

    }


    req = requests.post('https://api.sandbox.africastalking.com/version1/messaging', data=payload, headers=header)

    req = req.json()
    message_data = req['SMSMessageData']
    status = message_data["Recipients"][0]['status']

    return status
