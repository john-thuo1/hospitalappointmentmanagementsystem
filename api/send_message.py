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
        'apiKey': 'fa8c6d33e8cbffb38de8cee66c4df0336ab17610788b98e6db0135330ae18f60'

    }


    req = requests.post('https://api.sandbox.africastalking.com/version1/messaging', data=payload, headers=header)

    req = req.json()
    message_data = req['SMSMessageData']
    status = message_data["Recipients"][0]['status']

    return status
