from datetime import datetime,timezone,timedelta
from write_to_file import write_to_json, write_to_csv
from hashlib import sha256
import requests
import hmac
import os
import configparser
import hashlib
import urllib.parse
from version import VERSION

# 2. Function to get version from Git or fallback to version.py
SCRIPT_VERSION = VERSION # Update with the actual version of the script

# Display version on the terminal at script start
#print(f"\n=== Audit Export Client Version: {SCRIPT_VERSION} ===\n") # Uncomment to display the version at the start of the script


# Read configuration file
config = configparser.ConfigParser()

# Example  /Users/first.lastname/Desktop/audit-export-client-v2/config.ini
config.read('config.ini')   # Update with the actual path to your config.ini

# Set environment variables from config
api_token = config['DEFAULT']['API_TOKEN']
api_token_id = config['DEFAULT']['API_TOKEN_ID']

method = "GET"
path = "/audit/api/v1/events"
queryParams = ""
host = "api.virtru.com"


# Function to generate date intervals
# This function generates date intervals for making API requests
def generate_date_intervals(start_date, end_date, delta):
    current_date = start_date
    while current_date < end_date:
        interval_end = min(current_date + delta, end_date)
        yield (current_date, interval_end)
        current_date = interval_end

# Parsing start and end dates
#YYYY-MM-DD
start_date_str = '2025-01-01T00:00:00Z'  # This can be changed to any starting date
end_date_str = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ') # Get the current UTC date and time as an ISO 8601 formatted string (YYYY-MM-DDTHH:MM:SSZ).


start_date = datetime.fromisoformat(start_date_str.rstrip('Z'))
print("Start Date: ", start_date)
end_date = datetime.fromisoformat(end_date_str.rstrip('Z'))

# Set the interval length for data fetching. Adjust the timedelta value 
# to change the frequency of data retrieval. Uncomment the desired interval.
interval_length = timedelta(days=1)  # Example: 1 day interval
#interval_length = timedelta(hours=6)  # Fetches data in 6-hour chunks
#interval_length = timedelta(days=7)   # Fetches data in 1-week chunks
#interval_length = timedelta(hours=1)  # Fetches data in 1-hour chunks
#interval_length = timedelta(seconds=30)  # Fetches data in 30-second chunks

print("End Date: ", end_date)


# Define 'now' before using it in messageToSign
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

def _hash_string(string_to_hash):
    """Build an unseeded hash of a string."""
    return hashlib.sha256(str.encode(string_to_hash)).hexdigest()

def _build_string_to_hash(headers, path, query, method, body):
    """Construct the string with its new lines to sign."""
    header_string = (
        "content-type:"
        + headers["content-type"]
        + "\n"
        + "date:"
        + headers["date"]
        + "\n"
        + "host:"
        + headers["host"]
        + "\n"
    )

    string_to_hash = (
        method.upper()
        + "\n"
        + path
        + "\n"
        + query
        + "\n"
        + header_string
        + "\n"
        + "content-type;date;host"
        + "\n"
        + _hash_string(body)
    )

    return string_to_hash

def fetch_data(start_date, end_date, api_token, api_token_id, queryParams, output_dir='audit_output'):

    # Initialize an empty list to store data for each API request within a specific date range.
    # This list will collect the data retrieved from the API response for the given date interval
    # and will be reset for each new interval in the larger loop in the main part of the script.
    data = []
    nextBookmark = None  # Initialize nextBookmark
    max_iterations = 10  # Set a limit to the number of iterations
    current_iteration = 0

    while current_iteration < max_iterations:
        # Define 'now' for each request
        now = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')

        # Generate the body hash for each request
        bodyHex = sha256(str("").encode()).hexdigest()

        # Add bookmark to queryParams if it exists
        if nextBookmark is not None:
            queryParams = f"bookmark={urllib.parse.quote(nextBookmark)}&"
        
        queryParams = f"from={urllib.parse.quote(start_date)}&to={urllib.parse.quote(end_date)}"

        # Prepare the headers
        headers = {
            'accept': 'application/json',
            'date': now,
            'content-type': 'application/json; charset=utf-8',
            'host': host,
            'X-Request-Limit': '1000'
        }

        # Generate signature for each request
        string_hash = _build_string_to_hash(
            headers=headers,
            path=path + (f"?{queryParams}" if queryParams else ""),
            query=queryParams,
            method=method,
            body="",
        )

        signature = hmac.new(
            key=str.encode(api_token),
            msg=str.encode(string_hash),
            digestmod=hashlib.sha256,
        ).hexdigest()

        headers["X-Auth-Signedheaders"] = "content-type;date;host"
        headers["Authorization"] = "HMAC " + api_token_id + ":" + signature

        url = f"https://{host}{path}?{queryParams}"
        query = urllib.parse.urlsplit(url).query
        params = dict(urllib.parse.parse_qsl(query))

        try:
            response = requests.request(method, f"https://{host}{path}", headers=headers, params=params)
            if response.status_code != 200:
                print(f"Error fetching data: {response.status_code}, {response.text}")
                break

            response_data = response.json()
           
            #print(f"Full response: {response_data}")  # Log the full response for debugging
            data.extend(response_data.get('events', [])) # Extract events from the response

            nextBookmark = response_data.get('bookmarks', {}).get('nextBookmark')
            current_iteration += 1
            if not nextBookmark:
                print("No more bookmarks found. Stopping...")
                break

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            break

    return data

# Function to create required directories and subdirectories for JSON and CSV
def create_directories(base_dir='audit_output'):
    # Define paths for JSON and CSV subdirectories
    json_dir = os.path.join(base_dir, 'json_files')
    csv_dir = os.path.join(base_dir, 'csv_files')

    # Create base directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)


    # Create subdirectories for CSV and JSON if they don't exist
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    if not os.path.exists(json_dir):
       os.makedirs(json_dir)
 
create_directories()  # Call this function at the beginning of your main script

# Function to write data to files
def write_data_to_files(data, date_str, base_dir='audit_output'):
    # Define file paths using the date string for naming
    json_file_name = f'{date_str}.json'
    csv_file_name = f'{date_str}.csv'

    # Define paths for JSON and CSV files within their respective subdirectories
    json_file_path = os.path.join(base_dir, 'json_files', json_file_name)
    csv_file_path = os.path.join(base_dir, 'csv_files', csv_file_name)

    # Write data to JSON and CSV
    # Check if files already exist. Skip if they do.
    if not os.path.exists(json_file_path):
        write_to_json(data, json_file_path)
        print(f"Data for {date_str} written to {json_file_path}")
    else:
        print(f"JSON file for {date_str} already exists. Skipping.")

    if not os.path.exists(csv_file_path):
        write_to_csv(data, csv_file_path)
        print(f"Data for {date_str} written to {csv_file_path}")
    else:
        print(f"CSV file for {date_str} already exists. Skipping.")

# Loop for fetching and writing data
# Fetching data for each interval
# The interval_length is set (e.g., 1 day), but you can adjust this based on your needs.
# Loop through generated date intervals and fetch data for each interval
for interval_start, interval_end in generate_date_intervals(start_date, end_date, interval_length):
    # Format the dates for the current interval
    # Format the datetime objects to strings in ISO 8601 format
    formatted_start_date = interval_start.isoformat() + 'Z'
    formatted_end_date = interval_end.isoformat() + 'Z'

    # Fetch data for the current interval
    interval_data = fetch_data(formatted_start_date, formatted_end_date, api_token, api_token_id, queryParams)

    # Write data if it exists for the day
    # Check if data exists for the day, and if so, write to files
    if interval_data:
        date_str = interval_start.strftime('%Y-%m-%d')
        print(f"Number of records received for {date_str}: {len(interval_data)}")
        write_data_to_files(interval_data, date_str)
    else:
        print(f"No data received for interval starting {formatted_start_date}")



print("\n######################################################")
print("######################################################")
print("######################################################")
print("###                                               ####")
print("### See the 'audit_output' path for the audit file ###")
print("###                                               ####")
print("######################################################")
print("######################################################")
print("######################################################\n")