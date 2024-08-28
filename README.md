# Flight Deals Project

This Python project notifies users when a flight is found at a specific price. It integrates multiple APIs including Google Sheets (Sheety), a flight search API (Amadeus), and a messaging API (Twilio).

## Project Structure

The project is split into several files, each responsible for a distinct functionality:

1. **`notification_manager.py`**: Handles sending SMS notifications via Twilio.
2. **`data_manager.py`**: Interacts with Google Sheets using Sheety.
3. **`flight_search.py`**: Communicates with the Amadeus Flight Search API.
4. **`flight_data.py`**: Structures and processes flight data to find the cheapest option.

## Main Functionality

### Setup

- **Imports**: Imports necessary modules and classes for managing data, searching for flights, and sending notifications.
- **Instance Creation**:
  - `DataManager`: Manages interaction with Google Sheets.
  - `FlightSearch`: Handles interactions with the flight search API.
  - `NotificationManager`: Sends notifications about flight deals.

### Update Airport Codes

- **Retrieve Data**: Fetches destination data from Google Sheets using `DataManager`.
- **Update Codes**: Iterates through each destination to update missing IATA codes by calling `get_iata_code` from `FlightSearch` and updates the Google Sheet with new IATA codes.

### Search for Flights and Send Notifications

- Sets the date range for searching flights from the next day to six months later.
- Searches for flights from the origin location to each destination using `FlightSearch`.
- Identifies the cheapest flight using `find_cheapest_flight`.
- If the cheapest flight price is lower than the stored lowest price and is valid, sends a notification using `NotificationManager`.

## Notification Manager

### Key Components

- **Initialization (`__init__` method)**:
  - Loads Twilio credentials (`TWILIO_SID` and `TWILIO_AUTH_TOKEN`) from environment variables.
  - Initializes a Twilio Client object.

- **`send_message` Method**:
  - Sends a WhatsApp message with details about a low-priced flight.
  - Message includes price, origin location, destination, and travel dates.
  - Uses Twilio API to send the message from a specified WhatsApp number to a verified recipient's number.
  - Prints the message SID to confirm successful delivery.

## Data Manager

### Overview

- Manages interaction with a Google Sheet that stores flight destination data using the Sheety API.

### Key Methods

- **`get_destination_data`**:
  - Retrieves data from the Google Sheet and returns the destination data.

- **`updating_iata`**:
  - Updates IATA codes in the Google Sheet. Constructs a request body with the IATA code and performs a PUT request to update the table.

## Flight Search

### Overview

- Communicates with the Amadeus API to obtain flight information and airport codes. Handles token management and API requests.

### Key Methods

- **`__init__`**:
  - Loads API credentials (`AMADEUS_API_KEY` and `AMADEUS_SECRET`) from environment variables.
  - Calls `_get_new_token` to obtain an access token from the Amadeus API.

- **`get_iata_code`**:
  - Retrieves the IATA airport code for a given city.
  - Sends a request to the IATA Search API with the city name as a keyword.
  - Returns the IATA code or "N/A" if not found.

- **`_get_new_token`**:
  - Requests a new access token from the Amadeus API.
  - Prints the token and its expiration time for debugging.
  - Returns the access token.

- **`check_flights`**:
  - Searches for flight offers between origin and destination locations within a specified date range.
  - Handles responses and errors, and returns flight offers in JSON format if successful.

## Flight Data

### Overview

- Processes and structures flight data to identify the cheapest flight option from a list.

### Key Components

- **Initialization**:
  - Defines attributes to look for when searching for flights to provide exact flight data.

- **`find_cheapest_flight`**:
  - Checks if flight data is provided or not. If not, returns a `FlightData` object with "N/A" values.
  - Extracts details from the first flight to initialize the cheapest flight data.
  - Iterates through the list of flights to find the lowest price.
  - Prints the lowest price and destination.
  - Returns a `FlightData` object containing details of the cheapest flight found.
