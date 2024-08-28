import os
from twilio.rest import Client

from dotenv import load_dotenv

load_dotenv()

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(os.environ['TWILIO_SID'], os.environ["TWILIO_AUTH_TOKEN"])

    def send_message(self, price, origin_loc, to_loc, departure_date, arrival_date):
        message = self.client.messages.create(
            from_=os.environ["TWILIO_WHATSAPP_NUMBER"],
            body=f"Low Price alert! Only {price} to fly from {origin_loc} to {to_loc} on {departure_date} until {arrival_date}.",
            to=os.environ["TWILIO_VERIFIED_NUMBER"]
        )
        print(message.sid)
