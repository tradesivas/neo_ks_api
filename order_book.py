import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv(override=True)

# Define the endpoint and sId (server id)
order_book_endpoint = os.getenv("order_book_endpoint") + os.getenv("server_id")

# Define the order payload
order_book_payload = {}

# Set up headers
order_book_headers = {
    'accept': 'application/json',
    'Sid': os.getenv("session_id"),  # Session ID from .env
    'Auth': os.getenv("session_token"),  # Session token from .env
    'neo-fin-key': 'neotradeapi',  # Use appropriate key
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f"Bearer {os.getenv('app_access_token')}"  # Access token from .env
}

# Make the POST request to place the order
order_book_response = requests.get(order_book_endpoint, headers=order_book_headers, data=order_book_payload)
print(order_book_response.text)

# Check if the request was successful
if order_book_response.status_code == 200:
    # Parse the JSON response
    response_data = order_book_response.json()

    # Get the number of orders
    total_orders = len(response_data["data"])

    # Print the total number of orders
    print(f"Total number of orders: {total_orders}")
    
    # # Extract the order ID (nOrdNo)
    # order_id = response_data.get("nOrdNo")
    
    # if order_id:
    #     print(f"Order placed successfully! Order ID: {order_id}")
    # else:
    #     print("Order ID not found in the response.")
else:
    print(f"Failed to get order book. Status Code: {order_book_response.status_code}")
    print(f"Response: {order_book_response.text}")