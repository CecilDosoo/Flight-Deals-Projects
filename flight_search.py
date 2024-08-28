import requests
import os
from dotenv import load_dotenv

TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
IATA_SEARCH_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"

load_dotenv()
class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_SECRET"]
        self._token = self._get_new_token()

    def get_iata_code(self, city):
        header = {
            "Authorization": f"Bearer {self._token}"
        }
        parameters = {
            "keyword": city,
            "max": "2",
            "include": "AIRPORTS"
        }
        response = requests.get(url=IATA_SEARCH_ENDPOINT, params=parameters, headers=header)
        data = response.json()
        try:
            code = data["data"][0]["iataCode"]
        except IndexError:
            print("IndexError: No iataCode for airport")
            return "N/A"
        except KeyError:
            print("KeyError: No iataCode for airport")
            return "N/A"

        return code

    def _get_new_token(self):

        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)
        print(f"Your token is {response.json()['access_token']}")
        print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()['access_token']

    def check_flights(self, origin_loc, destination_loc, from_time, to_time):

        headers = {"Authorization": f"Bearer {self._token}"}

        query = {
            "originLocationCode": origin_loc,
            "destinationLocationCode": destination_loc,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
            "max": "5",
        }

        response = requests.get(
            url=FLIGHT_ENDPOINT,
            headers=headers,
            params=query,
        )
        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("Response body:", response.text)
            return None

        return response.json()
