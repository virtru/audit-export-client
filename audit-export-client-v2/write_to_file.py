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

def write_to_json(data, output_dir='audit_output'):
    output_dir_path = create_output_dir(output_dir)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(output_dir_path, f'output_{timestamp}.json')
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def write_to_csv(data, output_dir='audit_output'):
    
    # Define the fields for the CSV
    fields = ['id', 'object_type', 'object_id', 'object_name', 
              # Uncomment the object attribute field if needed
              #'object_attribute',
              'action_type', 'action_result', 
              'owner_id', 'owner_orgId', 'actor_id', 'client_info_userAgent', 'client_info_platform', 'client_info_requestIp', 'event_meta_data_type', 
              'event_meta_data_record_id', 'event_meta_data_record_type', 'timestamp', 
              'page', 'next_bookmark']

    # Create output directory
    output_dir_path = create_output_dir(output_dir)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(output_dir_path, f'output_{timestamp}.csv')

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for event in data['events']:
            row = {
                'id': event.get('id', ''),
                'object_type': event['object'].get('type', ''),
                'object_id': event['object'].get('id', ''),
                'object_name': event['object'].get('name', ''),
                # Uncomment the object attribute if needed
                #'object_attribute': event['object'].get('attributes', ''),
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
                'page': data.get('page', ''),
                'next_bookmark': data['bookmarks'].get('nextBookmark', '') if 'bookmarks' in data else ''
            }
            writer.writerow(row)

    # Returns a message if there is no data to write to the CSV 
    if 'events' not in data:
        print("\n\nNo events key found in data to write to the CSV file.")
        print("error: end date is incorrectly formatted or empty.")
        
    return


