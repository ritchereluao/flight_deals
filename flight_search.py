import requests
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = ""


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def get_destination_code(self, city_name):
        query = {
            "term": city_name,
            "location_types": "city",
        }
        headers = {
            "apikey": TEQUILA_API_KEY,
        }

        response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query", params=query, headers=headers)
        code = response.json()["locations"][0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {
            "apikey": TEQUILA_API_KEY,
        }
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "curr": "SGD",
        }

        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=query, headers=headers)
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights for {destination_city_code}.")

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][0]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: S${flight_data.price}")
        return flight_data
