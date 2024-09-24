import requests
import os
import json
from dotenv import load_dotenv
load_dotenv(override=True)
app_access_token_endpoint = os.getenv("app_access_token_endpoint")
scrip_master_endpoint = os.getenv("scrip_master_endpoint")
app_access_token = os.getenv("app_access_token")

# Define headers
scrip_master_headers = {
    'accept': '*/*',
    'Authorization': f'Bearer {app_access_token}'
}

# Make the GET request to fetch file paths
try:
    scrip_master_response = requests.get(scrip_master_endpoint, headers=scrip_master_headers)
    scrip_master_response.raise_for_status()  # Check for HTTP errors
    file_paths_response = scrip_master_response.json()

    # Extract file paths from the response
    file_paths = file_paths_response['data']['filesPaths']
    base_folder = file_paths_response['data']['baseFolder']
    
    # Print the file paths
    print("File Paths:", file_paths)
    
    # Map file paths to meaningful variable names
    file_paths_dict = {
        "BSE_CM_FILE_PATH": file_paths[0],
        "CDE_FO_FILE_PATH": file_paths[1],
        "MCX_FO_FILE_PATH": file_paths[2],
        "NSE_CM_FILE_PATH": file_paths[3],
        "NSE_FO_FILE_PATH": file_paths[4],
        "BSE_FO_FILE_PATH": file_paths[5],
        "BASE_FOLDER": base_folder
    }

    # Update the .env file with new file paths
    with open('.env', 'r') as file:
        file_data = file.read()

    # Replace or append new file paths in the .env file
    for key, value in file_paths_dict.items():
        if key in file_data:
            # Replace existing file path
            file_data = file_data.replace(f'{key}={os.getenv(key)}', f'{key}={value}')
        else:
            # Append new file path
            file_data += f'\n{key}={value}'

    # Write the updated content back to the .env file
    with open('.env', 'w') as file:
        file.write(file_data)

    print("File paths updated in .env file.")

    
except requests.exceptions.RequestException as e:
    print("Error fetching scrip master file paths:", e)

# List of file paths stored in the .env file
file_paths = [
    os.getenv("BSE_CM_FILE_PATH"),
    os.getenv("CDE_FO_FILE_PATH"),
    os.getenv("MCX_FO_FILE_PATH"),
    os.getenv("NSE_CM_FILE_PATH"),
    os.getenv("NSE_FO_FILE_PATH"),
    os.getenv("BSE_FO_FILE_PATH")
]

# Define a directory to save the downloaded files
download_directory = "scripmaster_files"
os.makedirs(download_directory, exist_ok=True)  # Create the directory if it doesn't exist

# Iterate over each file path and download the file
for file_url in file_paths:
    if file_url:  # Check if the file_url is not None
        try:
            response = requests.get(file_url)
            response.raise_for_status()  # Check for HTTP errors

            # Extract the filename from the URL
            filename = os.path.join(download_directory, file_url.split('/')[-1])

            # Save the content to a file
            with open(filename, 'wb') as file:
                file.write(response.content)

            print(f"Downloaded: {filename}")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading {file_url}: {e}")
    else:
        print("File URL is empty, skipping.")