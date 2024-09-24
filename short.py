import neo_api_client
from neo_api_client import NeoAPI
import os
import pandas as pd
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
df = pd.read_csv ("ks_cash_scripmaster.txt",sep="|", encoding='unicode_escape')
##############################################
def place_new_order(instrumentToken,qty):
    order_response = client.place_order(exchange_segment='NSE', product='MIS', price='0', order_type='MKT', quantity=qty, validity='DAY', trading_symbol=instrumentToken,
                    transaction_type='S', amo="NO", disclosed_quantity="0", market_protection="0", pf="N",
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
newotp= input("Enter NEW OTP: ")
################################################
try:
        session_response = client.session_2fa(OTP=newotp)
except Exception as e:
        print("Exception when calling SessionApi->session_2fa: %s\n" % e)
######################################################
instrumentName= input("[Short] Enter instrumentName: ")
instrumentToken = df.loc[(df['instrumentName'] == instrumentName) & (df['instrumentType'] == 'EQ') & (df['segment'] == 'CASH') & (df['exchange'] == 'NSE'), 'instrumentToken'].iloc[0]
instrumentToken = str(instrumentToken)
print("instrumentToken for " +instrumentName," :" +instrumentToken)
qty = input("[Short] Enter Quantity: ")
place_new_order(instrumentToken,qty)