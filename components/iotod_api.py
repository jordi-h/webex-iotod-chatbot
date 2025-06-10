"""This module contains the logic for Cisco IoT Operations Dashboard API integration."""

import requests

IOTOD_BASEURL = "https://eu.ciscoiot.com/nbapi"
ACCESS_TOKEN_EXPIRATION_TIME = 300

def translate_name_to_eid(organization_id, access_token, device_name):
    '''
    Translate device name to device EID using the device listing API.
    Important as most device related APIs need a device EID, not a name.
    '''
    # Get all devices from the API
    all_devices = get_all_devices(organization_id, access_token)

    if all_devices:
        # Loop through the devices to find a matching name
        for device in all_devices:
            # Compare device names
            if device['name'].lower() == device_name.lower():
                return device['eid']

    return None

def get_access_token(api_key_id, api_key):
    # Define the URL and the payload
    url = IOTOD_BASEURL+"/iam/v1/auth/token"
    payload = {
        "client_id": api_key_id,
        "client_secret": api_key,
        "grant_type": "client_credentials"
    }

    # Set the headers
    headers = {
        'Content-Type': 'application/json'
    }

    # Make the POST request
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        jsonResponse = response.json()
        token = jsonResponse.get("access_token")
        return token
    else:
        # Handle errors or unsuccessful requests
        print(f"Failed to obtain token, status code: {response.status_code}")
        return None

def get_all_devices(organization_id, access_token):
    # Define the URL
    url = IOTOD_BASEURL + "/edm/v1/devices"

    # Set the headers
    headers = {
        "Accept": "application/json",
        "x-tenant-id": organization_id,
        "Authorization": "Bearer " + access_token
    }

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        jsonResponse = response.json()
        devices_info = [{
            'name': device['name'],
            'status': device['status'],
            'deviceCategory': device['deviceCategory'],
            'deviceType': device['deviceType'],
            'eid': device['eid']
        } for device in jsonResponse.get('results', [])]
        return devices_info
    else:
        print(f"Failed to obtain devices, status code: {response.status_code}")
        return None

def get_device_details(organization_id, access_token, device_name):
    device_eid = translate_name_to_eid(organization_id, access_token, device_name)
    if not device_eid:
        return None
    
    # Define the URL
    url = IOTOD_BASEURL + f"/edm/v1/devices/{device_eid}"

    # Set the headers
    headers = {
        "Accept": "application/json",
        "x-tenant-id": organization_id,
        "Authorization": "Bearer " + access_token
    }

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        jsonResponse = response.json()
        device_details = {
            'name': jsonResponse.get('name', 'N/A'),
            'status': jsonResponse.get('status', 'N/A'),
            'lastHeard': jsonResponse.get('lastHeard', 'N/A'),
            'deviceCategory': jsonResponse.get('deviceCategory', 'N/A'),
            'deviceType': jsonResponse.get('deviceType', 'N/A'),
            'runningFirmwareVersion': jsonResponse.get('runningFirmwareVersion', 'N/A'),
            'ip': jsonResponse.get('ip', 'N/A'),
            'openIssues': jsonResponse.get('openIssues', 'N/A'),
            'labels': jsonResponse.get('labels', 'N/A'),
            'lat': jsonResponse.get('lat', 'N/A'),
            'lng': jsonResponse.get('lng', 'N/A'),
            'managedBy': jsonResponse.get('managedBy', 'N/A'),
            'eid': jsonResponse.get('eid', 'N/A'),
            'configGroup': jsonResponse.get('configGroup', 'N/A'),
            'configGroupId': jsonResponse.get('configGroupId', 'N/A'),
            'Up Time': jsonResponse.get('Up Time', 'N/A'),
            'SN': jsonResponse.get('SN', 'N/A'),
            'ioxIp': jsonResponse.get('ioxIp', 'N/A'),
            'fogdId': jsonResponse.get('fogdId', 'N/A'),
            'lastPnpSyncTimestamp': jsonResponse.get('lastPnpSyncTimestamp', 'N/A'),
            'pnpSyncError': jsonResponse.get('pnpSyncError', 'N/A'),
            'conflicted': jsonResponse.get('conflicted', False),
            'pid': jsonResponse.get('pid', 'N/A'),
            'adminUsername': jsonResponse.get('adminUsername', 'N/A'),
            'adminPassword': jsonResponse.get('adminPassword', 'N/A')
        }
        return device_details
    else:
        print(f"Failed to obtain device details, status code: {response.status_code}")
        return None
