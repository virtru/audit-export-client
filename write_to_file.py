# write_to_file.py
import os
import csv
import json
from datetime import datetime

def create_output_dir(output_dir='audit_output'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir_path = os.path.join(script_dir, output_dir)
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    return output_dir_path

def write_to_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def write_to_csv(events, file_path, buffer_size=1000):


    buffer = []
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'object_type', 'object_id', 'object_name', 'object_attribute', 'action_type', 'action_result', 'owner_id', 'owner_orgId', 'actor_id', 'client_info_userAgent', 'client_info_platform', 'client_info_requestIp', 'event_meta_data_type', 'event_meta_data_record_id', 'event_meta_data_record_type', 'timestamp'])
        writer.writeheader()

        for event in events:
            if not isinstance(event, dict):
                print(f"Unexpected data format for event: {event}")
                continue

            formatted_event = {
                'id': event.get('id', ''),
                    'object_type': event['object'].get('type', ''),
                    'object_id': event['object'].get('id', ''),
                    'object_name': event['object'].get('name', ''),
                    'action_type': event['action'].get('type', ''),
                    'action_result': event['action'].get('result', ''),
                    'owner_id': event['owner'].get('id', ''),
                    'owner_orgId': event['owner'].get('orgId', ''),
                    'actor_id': event['actor'].get('id', ''),
                    'client_info_userAgent': event['clientInfo'].get('userAgent', ''),
                    'client_info_platform': event['clientInfo'].get('platform', ''),
                    'client_info_requestIp': event['clientInfo'].get('requestIp', ''),
                    'event_meta_data_type': event['eventMetaData'].get('auditDataType', ''),
                    'event_meta_data_record_id': event['eventMetaData'].get('auditRecordId', ''),
                    'event_meta_data_record_type': event['eventMetaData'].get('auditRecordType', ''),
                    'timestamp': event.get('timestamp', ''),
            }
            buffer.append(formatted_event)
            if len(buffer) >= buffer_size:
                writer.writerows(buffer)
                buffer.clear()

        if buffer:
            writer.writerows(buffer)

    if not events:
        print("\nNo events to write to the CSV file.")
        print("error: end date is incorrectly formatted or empty.")
