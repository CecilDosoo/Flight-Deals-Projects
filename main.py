import time
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
import datetime
from notification_manager import NotificationManager

# ==================== Set up the Flight Search ====================

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.get_destination_data()
origin_loc = "LON"

# ==================== Update the Airport Codes in Google Sheet ====================

for data in sheet_data:
    if data["iataCode"] == "":
        city = data["city"]
        data["iataCode"] = flight_search.get_iata_code(city)
        # slowing down requests to avoid rate limit
        time.sleep(2)

data_manager.destination_data = sheet_data
data_manager.updating_iata()

# ==================== Search for Flights and Send Notifications ====================

tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
six_month_later = datetime.datetime.now() + datetime.timedelta(days=180)

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")
    flights = flight_search.check_flights(origin_loc, destination["iataCode"], tomorrow, six_month_later)
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        notification_manager.send_message(price=cheapest_flight.price,
                                          origin_loc=cheapest_flight.origin_airport,
                                          to_loc=cheapest_flight.destination_airport,
                                          departure_date=cheapest_flight.out_date,
                                          arrival_date=cheapest_flight.return_date)