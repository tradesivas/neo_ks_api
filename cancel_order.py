import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv(override=True)

# Define the endpoint and sId (server id)
cancel_order_endpoint = os.getenv("cancel_order_endpoint") + os.getenv("server_id")

# Define the order payload
cancel_order_details = {
    "on": "240925001327102", # order id
    "am": "NO"  # AMO(YES/NO)
}

# Convert the order details to a URL-encoded string
#place_order_payload = f"jData={requests.utils.quote(str(place_order_details))}"
cancel_order_payload = f"jData={requests.utils.quote(json.dumps(cancel_order_details))}"

# Set up headers
cancel_order_headers = {
    'accept': 'application/json',
    'Sid': os.getenv("session_id"),  # Session ID from .env
    'Auth': os.getenv("session_token"),  # Session token from .env
    'neo-fin-key': 'neotradeapi',  # Use appropriate key
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f"Bearer {os.getenv('app_access_token')}"  # Access token from .env
}

# Make the POST request to place the order
cancel_order_response = requests.post(cancel_order_endpoint, headers=cancel_order_headers, data=cancel_order_payload)

# Check if the request was successful
if cancel_order_response.status_code == 200:
    # Parse the JSON response
    response_data = cancel_order_response.json()
    
    # Extract the order ID (nOrdNo)
    order_id = response_data.get("result")
    
    if order_id:
        print(f"Order canceled successfully! Order ID: {order_id}")
    else:
        print("Order ID not found in the response.")
else:
    print(f"Failed to cancel order. Status Code: {cancel_order_response.status_code}")
    print(f"Response: {cancel_order_response.text}")