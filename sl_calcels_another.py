import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv(override=True)

# Define the endpoint and sId (server id)
order_history_endpoint = os.getenv("order_history_endpoint") + os.getenv("server_id")
cancel_order_endpoint = os.getenv("cancel_order_endpoint") + os.getenv("server_id")



# Get Order Ids for Stoploss Order and Target Order
sl_order_id = input("Enter Order ID for SL: ")
tg_order_id = input("Enter Order ID for TG: ")
# Define the order payload
sl_order_history_details = {
    "nOrdNo": sl_order_id
    }
sl_order_history_payload = f"jData={requests.utils.quote(json.dumps(sl_order_history_details))}"

# Set up headers
sl_order_history_headers = {
    'accept': 'application/json',
    'Sid': os.getenv("session_id"),  # Session ID from .env
    'Auth': os.getenv("session_token"),  # Session token from .env
    'neo-fin-key': 'neotradeapi',  # Use appropriate key
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f"Bearer {os.getenv('app_access_token')}"  # Access token from .env
}

# Make the POST request to place the order
sl_order_history_response = requests.post(order_history_endpoint, headers=sl_order_history_headers, data=sl_order_history_payload)
# print(sl_order_history_response.text)

# Check if the request was successful
if sl_order_history_response.status_code == 200:
    # Parse the JSON response
    response_data = sl_order_history_response.json()

    # Get the number of orders
    total_objects = len(response_data["data"])

    # Print the total number of orders
    print(f"Total number of objects: {total_objects}")
    
    # order status for stoploss order
    # Get the "ordSt" of the first object in the "data" array
    sl_order_status = response_data['data'][0]['ordSt']
    sym = response_data['data'][0]['sym']
    
    if sl_order_status == "complete":
        print(f"Stoploss Triggered for : {sym}")
    else:
        print(f"Stoploss NOT Triggered for : {sym}")
else:
    print(f"Failed to get order book. Status Code: {sl_order_history_response.status_code}")
    print(f"Response: {sl_order_history_response.text}")