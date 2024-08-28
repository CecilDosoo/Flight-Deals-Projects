import requests
import os
from dotenv import load_dotenv

load_dotenv()

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.prices_endpoint = os.environ["SHEETY_PRICES_ENDPOINT"]
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=self.prices_endpoint)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def updating_iata(self):
        for city in self.destination_data:
            body = {
                "price": {
                    "iataCode": city["iataCode"],
                }
            }
            response = requests.put(url=f"{self.prices_endpoint}/{city["id"]}", json=body)
            print(response.text)