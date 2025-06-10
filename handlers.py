# -*- coding: utf-8 -*-
"""This module contains handler functions."""

from .root import app
from .components.iotod_api import get_all_devices, get_device_details

def _truncate_at_substring(original_string, substring="->"):
    """Truncates a string at the specified substring."""
    if original_string is None:
        return None    
    parts = original_string.split(substring)    
    return parts[0]

@app.handle(intent='greet')
def greet(request, responder):
    prefix = ['Hello.', 'Hi.']
    responder.reply(prefix)

@app.handle(intent='exit')
def exit(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}
    responder.reply(['Bye!', 'Goodbye!', 'Have a nice day.', 'See you later.'])

@app.handle(intent='help')
def help(request, responder):
    """
    When the user asks for help, provide some sample queries they can try.
    """
    replies = ['This is what I can help you with: ...']
    responder.reply(replies)
    
@app.handle(intent='get_all_configuration_groups')
def getallconfigurationgroups(request, responder):
    responder.reply("get_all_configuration_groups intent.")
    
@app.handle(intent='get_all_alerts')
def getallalerts(request, responder):
    responder.reply("get_all_alerts intent.")
    
@app.handle(intent='get_all_events')
def getallevents(request, responder):
    responder.reply("get_all_events intent.")

@app.handle(intent='get_all_devices')
def getalldevices(request, responder):
    """
    Lists all the devices in the organization with their details in a readable format.
    """
    # api_details = request.context['user']['api_details'][0]
    # organization_id = api_details.get('organization_id', '')
    # access_token = api_details.get('access_token', '')
    # organization_name = _truncate_at_substring(api_details.get('api_key_id'), "->")

    # devices_info = get_all_devices(organization_id, access_token)

    # if not devices_info:
    #     responder.reply("I couldn't find any devices. "
    #             "This could have happened because something went wrong during communication with the IOT OD platform. "
    #             "Please retry, and if the issue persists, contact support.")
    #     return

    # organization_part = f" in the {organization_name} organization" if organization_name else ""
    # message_lines = [f"Here are the devices{organization_part}:"]
    # for device in devices_info:
    #     device_str = (
    #         f"Name: {device['name']}\n"
    #         f"  - Status: {device['status']}\n"
    #         f"  - Category: {device['deviceCategory']}\n"
    #         f"  - Type: {device['deviceType']}\n"
    #         f"  - EID: {device['eid']}"
    #     )
    #     message_lines.append(device_str)

    # message = "\n".join(message_lines)

    # responder.reply(message)
    responder.reply("get_all_devices intent.")

@app.handle(intent='get_all_device_locations')
def getalldevicelocations(request, responder):
    responder.reply("get_all_device_locations intent.")
    
@app.handle(intent='get_all_device_applications')
def getalldeviceapplications(request, responder):
    responder.reply("get_all_device_applications intent.")
    
# e.g. query: What is up with device BT-1101
@app.handle(intent='get_device_by_name')
def getdevicebyname(request, responder):
    """
    Provide details on a given device.
    """
    # api_details = request.context['user']['api_details'][0]
    # organization_id = api_details.get('organization_id', '')
    # access_token = api_details.get('access_token', '')
    # organization_name = _truncate_at_substring(api_details.get('api_key_id'), "->")

    # device_name_entity = next((e for e in request.entities if e.get('type') == 'devicename'), None)

    # # To extract the 'text' value from the found entity (if any)
    # device_name = device_name_entity.get('text') if device_name_entity else None

    # if device_name is None:
    #     responder.reply("I did not quite catch the device name. Can you repeat?"
    #                     "If the issue persists, contact support.")
    #     return
    
    # device_details = get_device_details(organization_id, access_token, device_name)

    # if not device_details:
    #     responder.reply("I couldn't find any device details. "
    #             "This could have happened because something went wrong during communication with the IOT OD platform or the device does not exist in your organization. "
    #             "Please retry, and if the issue persists, contact support.")
    #     return
    
    # organization_part = f" in the {organization_name} organization" if organization_name else ""
    # message_lines = [
    #     f"Here are the details about device {device_details['name']}{organization_part}:",
    #     f"  - Status: {device_details['status']}",
    #     f"  - Last Heard: {device_details['lastHeard']}",
    #     f"  - Category: {device_details['deviceCategory']}",
    #     f"  - Type: {device_details['deviceType']}",
    #     f"  - Running Firmware Version: {device_details['runningFirmwareVersion']}",
    #     f"  - IP: {device_details['ip']}",
    #     f"  - Open Issues: {device_details['openIssues']}",
    #     f"  - Labels: {device_details['labels']}",
    #     f"  - Latitude: {device_details['lat']}",
    #     f"  - Longitude: {device_details['lng']}",
    #     f"  - Managed By: {device_details['managedBy']}",
    #     f"  - EID: {device_details['eid']}",
    #     f"  - Config Group: {device_details['configGroup']}",
    #     f"  - Config Group ID: {device_details['configGroupId']}",
    #     f"  - Up Time: {device_details['Up Time']}",
    #     f"  - Serial Number: {device_details['SN']}",
    #     f"  - IOX IP: {device_details['ioxIp']}",
    #     f"  - Fogd ID: {device_details['fogdId']}",
    #     f"  - Last PnP Sync Timestamp: {device_details['lastPnpSyncTimestamp']}",
    #     f"  - PnP Sync Error: {device_details['pnpSyncError']}",
    #     f"  - Conflicted: {device_details['conflicted']}",
    #     f"  - PID: {device_details['pid']}",
    #     f"  - Admin Username: {device_details['adminUsername']}",
    #     f"  - Admin Password: {device_details['adminPassword']}"
    # ]

    # message = "\n".join(message_lines)

    # responder.reply(message)
    device_name_entity = next((e for e in request.entities if e.get('type') == 'devicename'), None)

    # To extract the 'text' value from the found entity (if any)
    device_name = device_name_entity.get('text') if device_name_entity else None

    if device_name is None:
        responder.reply("I did not quite catch the device name. Can you repeat?"
                        "If the issue persists, contact support.")
        return
    
    responder.reply("get_device_by_name intent" + " and device name is " + device_name + ".")
