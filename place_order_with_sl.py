import requests
import os
from dotenv import load_dotenv
import json
import time
import pandas as pd
import tvDatafeed
from tvDatafeed import TvDatafeed,Interval
from datetime import date, time, datetime as dt

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

#read scripmaster file
nse_cm = pd.read_csv (r"scripmaster_files\nse_cm.csv",sep=",")
# Load environment variables
load_dotenv(override=True)

# Define the endpoint and sId (server id)
place_order_endpoint = os.getenv("place_order_endpoint") + os.getenv("server_id")
stop_amount_per_trade = os.getenv("stop_amount_per_trade")
symbol = input("Enter Symbol: ")
tt = input("Buy or Sell (B/S): ")
pTrdSymbol  = nse_cm.loc[(nse_cm['pSymbolName'] == symbol.upper()) & (nse_cm['pGroup'] == 'EQ') & (nse_cm['pExchSeg'] == 'nse_cm') & (nse_cm['pSegment'] == 'CASH'), 'pTrdSymbol'].iloc[0]
#######        Position Sizing     #################
todays_date = date.today()
todays_date = date.today()
tdate = str(todays_date.year)+'-'+str(todays_date.month)+'-'+str(todays_date.day)
data = TvDatafeed().get_hist(symbol=symbol,exchange='NSE',interval=Interval.in_daily,n_bars=1)
ltp= data.loc[tdate+' 09:15:00']['close']
print(f"LTP for {pTrdSymbol}: {ltp}")
sl = input("Enter stoploss Price: ")
if tt == "b":
    qty = str(int(float(stop_amount_per_trade)/(float(ltp)-float(sl))))
elif tt == "s":
    qty = str(int(float(stop_amount_per_trade)/(float(sl)-float(ltp))))

print(f"qty = {qty}")
##################################################

if int(qty) > 0:

    # Define the order payload
    place_order_details = {
        "am": "NO",  # AMO(YES/NO)
        "dq": "0",  # Disclosed quantity
        "es": "nse_cm",  # Exchange segment
        "mp": "0",  # Market Protection
        "pc": "MIS",  # Product code
        "pf": "N",  # PosSqrFlg
        "pr": "0",  # Price
        "pt": "MKT",  # Order Type
        "qt": qty,  # Quantity
        "rt": "DAY",  # Order Duration
        "tp": "0",  # Trigger price
        "ts": pTrdSymbol,  # Trading Symbol
        "tt": tt.upper()  # Transaction Type
    }
    # Define the Stoploss order payload
    if tt.upper() == "B":
        sl_tt = "S"
    else:
        sl_tt = "B"
    sl_order_details = {
        "am": "NO",  # AMO(YES/NO)
        "dq": "0",  # Disclosed quantity
        "es": "nse_cm",  # Exchange segment
        "mp": "0",  # Market Protection
        "pc": "MIS",  # Product code
        "pf": "N",  # PosSqrFlg
        "pr": "0",  # Price
        "pt": "SL-M",  # Order Type
        "qt": qty,  # Quantity
        "rt": "DAY",  # Order Duration
        "tp": sl,  # Trigger price
        "ts": pTrdSymbol,  # Trading Symbol
        "tt": sl_tt  # Transaction Type
    }

    # Convert the order details to a URL-encoded string
    place_order_payload = f"jData={requests.utils.quote(json.dumps(place_order_details))}"
    sl_order_payload = f"jData={requests.utils.quote(json.dumps(sl_order_details))}"

    # Set up headers
    place_order_headers = {
        'accept': 'application/json',
        'Sid': os.getenv("session_id"),  # Session ID from .env
        'Auth': os.getenv("session_token"),  # Session token from .env
        'neo-fin-key': 'neotradeapi',  # Use appropriate key
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f"Bearer {os.getenv('app_access_token')}"  # Access token from .env
    }

    # Make the POST request to place the order
    place_order_response = requests.post(place_order_endpoint, headers=place_order_headers, data=place_order_payload)

    # Check if the request was successful
    if place_order_response.status_code == 200:
        # Parse the JSON response
        response_data = place_order_response.json()
        
        # Extract the order ID (nOrdNo)
        order_id = response_data.get("nOrdNo")
        
        if order_id:
            time.sleep(2)
            place_order_status = order_history(order_id)
            if place_order_status == "complete":

                print(f"Order placed successfully! Order ID: {order_id} Status: {place_order_status}")
                sl_order_response = requests.post(place_order_endpoint, headers=place_order_headers, data=sl_order_payload)
                if sl_order_response.status_code == 200:
                    # Parse the JSON response
                    response_data = sl_order_response.json()
                    
                    # Extract the order ID (nOrdNo)
                    order_id = response_data.get("nOrdNo")
                    
                    if order_id:
                        sl_order_status = order_history(order_id)
                        print(f"SL Order placed successfully! Order ID: {order_id} Status: {sl_order_status}")
                        
                    else:
                        print("SL Order ID not found in the SL order response.")
            else:
                print(f"Order placed successfully! Order ID: {order_id} Status: {place_order_status}")
                print("Stoploss order not placed")
        else:
            print("Place Order ID not found in the place order response.")
    else:
        print(f"Failed to place order. Status Code: {place_order_response.status_code}")
        print(f"Response: {place_order_response.text}")

else:
    print(" No orders were placed")