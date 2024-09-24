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

load_dotenv(override=True)
app_access_token_endpoint = os.getenv("app_access_token_endpoint")
login_validate_endpoint = os.getenv("login_validate_endpoint")
otp_generation_endpoint = os.getenv("otp_generation_endpoint")
scrip_master_endpoint = os.getenv("scrip_master_endpoint")
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
app_access_token = os.getenv("app_access_token")
view_token = os.getenv("view_token")
session_token = os.getenv("session_token")
Sid = os.getenv("Sid")
refresh_token = os.getenv("refresh_token")
user_access_token = os.getenv("user_access_token")
trade_userid = os.getenv("trade_userid")
trade_mobilenumber = os.getenv("trade_mobilenumber")
trade_password = os.getenv("trade_password")
view_token_user_id = os.getenv("view_token_user_id")

# Combine them into the format consumer-key:consumer-secret
api_credentials = f"{consumer_key}:{consumer_secret}"
# Encode the credentials in Base64
encoded_api_credentials = base64.b64encode(api_credentials.encode()).decode()

# Define the payload as a string, not a dictionary (for form encoding)
app_access_token_payload = 'grant_type=client_credentials'

# Set the headers with the Base64 encoded credentials
app_access_token_headers = {
    'Authorization': f'Basic {encoded_api_credentials}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Make the request to obtain the access token
try:
    app_access_token_response = requests.post(app_access_token_endpoint, headers=app_access_token_headers, data=app_access_token_payload)
    app_access_token_response.raise_for_status()  # Raise an error for bad responses

    # Extract access token from the response
    app_access_token = app_access_token_response.json().get('access_token')
    
    if app_access_token:
        print("App Access Token:", app_access_token)

        # Update the .env file with the new access token
        with open(".env", 'r') as file:
            filedata = file.read()
        
        # Replace old token in .env file
        filedata = filedata.replace(os.getenv("app_access_token"), app_access_token)

        with open(".env", 'w') as file:
            file.write(filedata)
    else:
        print("Access token not found in response.")

except requests.exceptions.RequestException as e:
    print("Error obtaining access token:", e)
# Define the payload using the environment variables
login_payload = json.dumps({
    "mobileNumber": trade_mobilenumber,
    "password": trade_password
})

# Define the headers using the access token from the environment
login_headers = {
    'accept': '*/*',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {app_access_token}'
}

# Make the request
try:
    login_response = requests.post(login_validate_endpoint, headers=login_headers, data=login_payload)
    login_response.raise_for_status()  # Raise an error for bad responses

    # Print the response
    print("Login Response:", login_response.json())
except requests.exceptions.RequestException as e:
    print("Error during login request:", e)

# Assuming login_response is the response you received
login_response_data = login_response.json()

# Extract the token
view_token = login_response_data.get('data', {}).get('token')
sid = login_response_data.get('data', {}).get('sid')

if view_token:
    print("View Token:", view_token)

    # Update the .env file with the new view token
    with open(".env", 'r') as file:
        filedata = file.read()

    # Replace old view token in .env file
    old_view_token = os.getenv("view_token")
    filedata = filedata.replace(old_view_token, view_token)

    with open(".env", 'w') as file:
        file.write(filedata)
else:
    print("View token not found in the response.")

# Decode the view token to get the user ID
try:
    decoded_view_token = jwt.decode(view_token, options={"verify_signature": False})  # Skip signature verification
    view_token_user_id = decoded_view_token.get("sub")
except Exception as e:
    print("Error decoding the view token:", e)

if view_token_user_id:
    # Define the payload
    otp_payload = json.dumps({
        "userId": view_token_user_id,
        "sendEmail": True,
        "isWhitelisted": True
    })

    # Set the headers using the view token
    otp_headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {app_access_token}',
        'Content-Type': 'application/json'
    }

    # Make the request to generate the OTP
    try:
        otp_response = requests.post(otp_generation_endpoint, headers=otp_headers, data=otp_payload)
        otp_response.raise_for_status()  # Raise an error for bad responses
        
        # Print the response
        print("OTP Generation Response:", otp_response.json())
        
    except requests.exceptions.RequestException as e:
        print("Error generating OTP:", e)
else:
    print("View Token User ID could not be retrieved from the view token.")

newotp= input("Enter NEW OTP: ")
session_payload = json.dumps({
  "userId": view_token_user_id,
  "otp": newotp
})
session_headers = {
  'accept': '*/*',
  'sid': sid,
  'Auth': view_token,
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {app_access_token}'
}

session_response = requests.request("POST", login_validate_endpoint, headers=session_headers, data=session_payload)

print(session_response.text)

# Assuming session_response is the response you received
session_response_data = session_response.json()

# Extract the session token
session_token = session_response_data.get('data', {}).get('token')
session_id = session_response_data.get('data', {}).get('sid')
server_id = session_response_data.get('data', {}).get('hsServerId')

if session_token:

    # Define the .env file path
    env_file_path = ".env"

    # Read the existing .env file
    with open(env_file_path, 'r') as file:
        filedata = file.read()

    # Replace or add the session token
    old_session_token = os.getenv("session_token")
    if old_session_token:
        filedata = filedata.replace(old_session_token, session_token)
    else:
        filedata += f"\nsession_token={session_token}"

    # Replace or add the SID
    old_session_id = os.getenv("session_id")
    if old_session_id:
        filedata = filedata.replace(old_session_id, session_id)
    else:
        filedata += f"\nsession_id={session_id}"

    # Replace or add the hsServerId
    old_server_id = os.getenv("server_id")
    if old_server_id:
        filedata = filedata.replace(old_server_id, server_id)
    else:
        filedata += f"\nserver_id={server_id}"

    # Write the updated data back to the .env file
    with open(env_file_path, 'w') as file:
        file.write(filedata)

    print("Session token, Session Id, and server Id stored successfully.")
    
else:
    print("Session token not found in the response.")