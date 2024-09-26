import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv(override=True)

# Define the endpoint and sId (server id)
modify_order_endpoint = os.getenv("modify_order_endpoint") + os.getenv("server_id")

# Define the order payload
modify_order_details = {
    "no": "240925001327102", # order id
    "tk": "2963", # pSymbol in scrip master
    "dd": "NA", # DateDays
    "vd": "DAY", # validity
    # "am": "NO",  # AMO(YES/NO)
    "dq": "0",  # Disclosed quantity
    "es": "nse_cm",  # Exchange segment
    "mp": "0",  # Market Protection
    "pc": "MIS",  # Product code
    # "pf": "N",  # PosSqrFlg
    "pr": "132.30",  # Price
    "pt": "L",  # Order Type
    "qt": "1",  # Quantity
    # "rt": "DAY",  # Order Duration
    "tp": "0",  # Trigger price
    "ts": "SAIL-EQ",  # Trading Symbol
    "tt": "B"  # Transaction Type
}

# Convert the order details to a URL-encoded string
#place_order_payload = f"jData={requests.utils.quote(str(place_order_details))}"
modify_order_payload = f"jData={requests.utils.quote(json.dumps(modify_order_details))}"

# Set up headers
modify_order_headers = {
    'accept': 'application/json',
    'Sid': os.getenv("session_id"),  # Session ID from .env
    'Auth': os.getenv("session_token"),  # Session token from .env
    'neo-fin-key': 'neotradeapi',  # Use appropriate key
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f"Bearer {os.getenv('app_access_token')}"  # Access token from .env
}

# Make the POST request to place the order
modify_order_response = requests.post(modify_order_endpoint, headers=modify_order_headers, data=modify_order_payload)

# Check if the request was successful
if modify_order_response.status_code == 200:
    # Parse the JSON response
    response_data = modify_order_response.json()
    
    # Extract the order ID (nOrdNo)
    order_id = response_data.get("nOrdNo")
    
    if order_id:
        print(f"Order modified successfully! Order ID: {order_id}")
    else:
        print("Order ID not found in the response.")
else:
    print(f"Failed to modify order. Status Code: {modify_order_response.status_code}")
    print(f"Response: {modify_order_response.text}")