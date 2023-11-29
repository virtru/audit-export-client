from datetime import datetime,timezone
from write_to_file import write_to_json, write_to_csv
from hashlib import sha256
import requests
import hmac
import os
import configparser
#dont worry syslog export option
# Call the function to update the config
#update_config()

# Read configuration file
config = configparser.ConfigParser()
# Update with the actual path to your config.ini
# Example  /Users/first.lastname/Desktop/audit-export-client-v2/config.ini
config.read('config.ini')  

# Set environment variables from config
api_token = config['DEFAULT']['API_TOKEN']
api_token_id = config['DEFAULT']['API_TOKEN_ID']

method = "GET"
path = "/audit/api/v1/events"
queryParams = ""
host = "api.virtru.com"


def get_date_input(prompt, end_date_check=False):
    while True:
        date_str = input(prompt)
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            if end_date_check and date.date() > datetime.now().date():
                print("Error: The entered date is in the future. Please enter a date that is not later than today.")
            else:
                return date.strftime('%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

start_date = get_date_input("Enter start date (YYYY-MM-DD): ")

# Uncomment end_date to prompt the user to input the end date
#end_date = datetime.now(timezone.utc).strftime('%Y-%m-%dT00:00:00Z')


end_date = datetime.now(timezone.utc).strftime('%Y-%m-%dT00:00:00Z')
print("End Date: ", end_date)

now = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')

payload={}

# Has Empty Body
hash = sha256(str("").encode())
bodyHex = hash.hexdigest()
messageToSign = """{0}
{1}
{2}
content-type:application/json; charset=utf-8
date:{3}
host:{4}

content-type;date;host
{5}""".format(method,path,queryParams,now,host,bodyHex)

signature = hmac.new(api_token.encode(), messageToSign.encode(), sha256).hexdigest()

headers = {
  'Authorization': 'HMAC {0}:{1}'.format(api_token_id, signature),
  'accept': 'application/json',
  'X-Request-Limit': '10',
  'X-Request-Page': '1',
  'X-Request-Start-Date': start_date,
  'X-Request-End-Date': end_date,
  #'X-Request-Start-Date': '2023-11-12T00:00:00Z',
  #'X-Request-End-Date': '2023-11-15T00:00:00Z',
  'Date': now,
  'Content-Type': 'application/json; charset=utf-8',
  'X-Auth-Signedheaders': 'content-type;date;host',
  'objectType': 'data_object',
  'objectType': 'user_object',
  'objectType': 'rule_object',
  'objectType': 'unit_attribute_object',
  'objectType': 'organization_object',
  'objectType': 'attribute_object',
  'Host':host
}

response = requests.request(method, "https://{0}{1}".format(host,path), headers=headers, data=payload)



response_data = response.json()

# Call the function from write_to_file.py
# Process the response
response_data = response.json()

# Define file paths
json_file_path = os.path.join('audit_output', 'output.json')
csv_file_path = os.path.join('audit_output', 'output.csv')

# Write to JSON
write_to_json(response_data, json_file_path)

# Write to CSV
write_to_csv(response_data, csv_file_path)

print("\n######################################################")
print("######################################################")
print("######################################################")
print("###                                               ####")
print("### See the 'audit_output' path for the audit file ###")
print("###                                               ####")
print("######################################################")
print("######################################################")
print("######################################################\n")
