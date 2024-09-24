import neo_api_client
from neo_api_client import NeoAPI
import os
from dotenv import load_dotenv
import pandas as pd
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
import base64
import time
import json
import jwt  # Make sure to install PyJWT
# Defining the host is optional and defaults to https://tradeapi.kotaksecurities.com/apim
# See configuration.py for a list of all supported configuration parameters.
load_dotenv()
app_access_token_endpoint = os.getenv("app_access_token_endpoint")
login_validate_endpoint = os.getenv("login_validate_endpoint")
otp_generation_endpoint = os.getenv("otp_generation_endpoint")
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
app_access_token = os.getenv("app_access_token")
view_token = os.getenv("view_token")
refresh_token = os.getenv("refresh_token")
user_access_token = os.getenv("user_access_token")
trade_userid = os.getenv("trade_userid")
trade_mobilenumber = os.getenv("trade_mobilenumber")
trade_password = os.getenv("trade_password")
view_token_user_id = os.getenv("view_token_user_id")

app_access_token_response = NeoAPI(consumer_key=consumer_key, consumer_secret=consumer_secret, 
                environment='prod')

# Login using password
try:
    login_response = app_access_token_response.login(mobilenumber=trade_mobilenumber, password=trade_password)
    print("---------------login response---------------")
    print(login_response)
    print("---------------End of login response---------------")
except Exception as e:
    print("Exception when calling SessionApi->login: %s\n" % e)

newotp= input("Enter NEW OTP: ")

#Generated session token
try:
        session_response = app_access_token_response.session_2fa(OTP=newotp)
        print("---------------session response---------------")
        print(session_response)
        print("---------------End of session response---------------")
except Exception as e:
        print("Exception when calling SessionApi->session_2fa: %s\n" % e)

logout_response = app_access_token_response.logout()
print("---------------logout response---------------")
print(logout_response)
print("---------------End of logout response---------------")
#Storing New OPT to .env file
oldotp = os.getenv("otp")
with open(".env",'r') as file :
        filedata = file.read()
filedata = filedata.replace(oldotp,newotp)
with open(".env",'w') as file :
        file.write(filedata)