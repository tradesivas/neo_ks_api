import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd
import tvDatafeed
from tvDatafeed import TvDatafeed,Interval
from datetime import date, time, datetime as dt

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

# Convert the order details to a URL-encoded string
#place_order_payload = f"jData={requests.utils.quote(str(place_order_details))}"
place_order_payload = f"jData={requests.utils.quote(json.dumps(place_order_details))}"

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
        print(f"Order placed successfully! Order ID: {order_id}")
    else:
        print("Order ID not found in the response.")
else:
    print(f"Failed to place order. Status Code: {place_order_response.status_code}")
    print(f"Response: {place_order_response.text}")