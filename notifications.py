from twilio.rest import Client
from twilio_account import *

class Notifications:
    def __init__(self):
        self.account_sid = get_account_sid()
        self.auth_token = get_auth_token()
        self.phone_number = get_phone_number()
        self.client = Client(self.account_sid, self.auth_token)

    ## phone numbers: "+1**********" ---> +1 represents country code
    def send_msg(self, phone_number, msg):
        client = self.client
        message = client.messages.create(
            to=phone_number,
            from_=self.phone_number,
            body=msg
        )
