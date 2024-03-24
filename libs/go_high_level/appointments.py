import requests
import os
from dotenv import load_dotenv

url = "https://rest.gohighlevel.com/v1/appointments/"

load_dotenv()

auth_token = os.getenv("GO_HIGH_LEVEL_AUTH_TOKEN")

headers = {
  'Authorization': f'Bearer {auth_token}',
}


def create_appointment(
        calendar_id: str,
        selected_timezone: str,
        selected_slot: str,
        email: str,
        phone: str
        ):
    payload = {
        "calendarId": calendar_id,
        "selectedTimezone": selected_timezone,
        "selectedSlot": selected_slot,    
        "email": email,
        "phone": phone
        }
    # response = requests.request("POST", url, headers=headers, data = payload)
    mock_response = {
        "id": "12345",
        "calendarId": calendar_id,
        "selectedTimezone": selected_timezone,
        "selectedSlot": selected_slot,    
        "email": email,
        "phone": phone
    }
    return mock_response

