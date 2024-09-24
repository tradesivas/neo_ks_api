import neo_api_client
from neo_api_client import NeoAPI
import os
from dotenv import load_dotenv
load_dotenv()
################################################
access_token = os.getenv("access_token")
userid = os.getenv("userid")
mobilenumber = os.getenv("mobilenumber")
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
password = os.getenv("password")
host = os.getenv("host")
##############################################
def place_new_order(qty):
    client.place_order(exchange_segment='NSE', product='INTRADAY', price='0', order_type='MKT', quantity=qty, validity='DAY', trading_symbol='',
                    transaction_type='B', amo="NO", disclosed_quantity="0", market_protection="0", pf="N",
                    trigger_price="0", tag=None)
##############################################
client = NeoAPI(consumer_key=consumer_key, consumer_secret=consumer_secret, 
                environment='prod')
try:
    login_response = client.login(mobilenumber=mobilenumber, password=password)
    print("---------------login response---------------")
    print(login_response)
    print("---------------End of login response---------------")
except Exception as e:
    print("Exception when calling SessionApi->login: %s\n" % e)
################################################
tg_or_id = input("Enter Target order id: ")
high = input("Enter Swing High Price: ")
####################################################
try:
        session_response = client.session_2fa(OTP=newotp)
except Exception as e:
        print("Exception when calling SessionApi->session_2fa: %s\n" % e)
######################################################