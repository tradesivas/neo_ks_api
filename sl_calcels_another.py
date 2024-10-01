import requests
import os
from dotenv import load_dotenv
import json
import time

def order_history(order_id):
    load_dotenv(override=True)
    order_history_endpoint = os.getenv("order_history_endpoint") + os.getenv("server_id")
    order_history_details = {
        "nOrdNo": order_id
        }
    order_history_payload = f"jData={requests.utils.quote(json.dumps(order_history_details))}"
    # Set up headers
    order_history_headers = {
        'accept': 'application/json',
        'Sid': os.getenv("session_id"),  # Session ID from .env
        'Auth': os.getenv("session_token"),  # Session token from .env
        'neo-fin-key': 'neotradeapi',  # Use appropriate key
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f"Bearer {os.getenv('app_access_token')}"  # Access token from .env
        }

    is_order_history_response = False
    while is_order_history_response == False:
        try:
            # Make the POST request to place the order
            order_history_response = requests.post(order_history_endpoint, headers=order_history_headers, data=order_history_payload)
            # print(sl_cancel_order_response.text)
            if order_history_response.status_code == 200:
                is_order_history_response = True
                response_data = order_history_response.json()
              
                # order status
                # Get the "ordSt" of the first object in the "data" array
                order_status = response_data['data'][0]['ordSt']
                sym = response_data['data'][0]['sym']
                
            else:
                print(f"Failed to get order book. Status Code: {order_history_response.status_code}")
                print(f"Response: {order_history_response.text}")
        except:
            print("waiting for internet!")
            time.sleep(5)
    return (order_status)

def cancel_order(order_id):
    load_dotenv(override=True)
    cancel_order_endpoint = os.getenv("cancel_order_endpoint") + os.getenv("server_id")
    cancel_order_details = {
         "on": order_id, # order id
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
    is_cancel_order_response = False
    while is_cancel_order_response == False:

        try:
            # Make the POST request to place the order
            cancel_order_response = requests.post(cancel_order_endpoint, headers=cancel_order_headers, data=cancel_order_payload)
            # print(sl_cancel_order_response.text)
            if cancel_order_response.status_code == 200:
                is_cancel_order_response = True
                response_data = cancel_order_response.json()
               
                # order status
                # Get the "ordSt" of the first object in the "data" array
                cancelled_order_id = response_data.get("result")
                print(f"Order cancelled for order id : {cancelled_order_id}")
                
            else:
                print(f"Failed to get order book. Status Code: {cancel_order_response.status_code}")
                print(f"Response: {cancel_order_response.text}")
        except:
            print("waiting for internet!")
            time.sleep(5)
    return (cancelled_order_id)

# Get Order Ids for Stoploss Order and Target Order
sl_order_id = input("Enter Order ID for SL: ")
tg_order_id = input("Enter Order ID for TG: ")

is_trade_closed = False

while is_trade_closed == False:
    print("---------------------------------------")
    print("")
    print("entering to While loop")
    print("getting order status for Stoploos order")
    sl_order_status = order_history(sl_order_id)
    print("getting order status for Target order")
    tg_order_status = order_history(tg_order_id)
    print("checking both order status is not complete")
    if (sl_order_status != "complete") and (tg_order_status != "complete"):
        print("No orders were hit")
        print("waiting to check again")
        time.sleep(5)
    elif (sl_order_status == "complete") and (tg_order_status == "cancelled"):
        print("Stoploss Hit")
        print("Target order already cancelled")
        is_trade_closed = True
    elif (sl_order_status == "cancelled") and (tg_order_status == "complete"):
        print("Target Hit")
        print("Stoploss order already cancelled")
        is_trade_closed = True
    else:
        print("one of the order was hit")
        print("checking whether stoploss order hit")
        if sl_order_status == "complete":
            print("Stop Loss Triggered")
            print("cancelling Target order...")
            cancelled_order_id = cancel_order(tg_order_id)
            print("Target order Cancelled")
            is_trade_closed = True
        elif tg_order_status == "complete":
            print("stoploss order not hit")
            print("Target Hit")
            print("cancelling stoploss order...")
            cancelled_order_id = cancel_order(sl_order_id)
            print("Stoploss order Cancenled")
            is_trade_closed = True
print("")
print("-----------------")
print("   End of Code   ")
print("-----------------")
print("")