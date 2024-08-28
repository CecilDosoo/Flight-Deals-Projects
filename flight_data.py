
class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, origin, destination, out_date, return_date):
        self.price = price
        self.origin_airport = origin
        self.destination_airport = destination
        self.out_date = out_date
        self.return_date = return_date

def find_cheapest_flight(flights):
    if flights is None or not flights['data']:
        print("No flight data")
        return FlightData(" N/A", "N/A", "N/A", "N/A", "N/A")

    first_flight = flights['data'][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)

    for flight in flights["data"]:
        price = float(flight["price"]["grandTotal"])
        if price < lowest_price:
            lowest_price = price
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)
            print(f"Lowest price to {destination} is £{lowest_price}")

    return cheapest_flight

