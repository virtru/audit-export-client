# 1. Imports and initial setup
from datetime import datetime, timezone, timedelta  # Manages date and time operations, including intervals
from write_to_file import write_to_json, write_to_csv  # Custom functions for writing data into JSON and CSV files
from hashlib import sha256  # For generating hash values
import requests  # Enables HTTP requests to call external APIs
import hmac  # Generates HMAC signatures for verifying API request authenticity
import os  # Interacts with the operating system (e.g., file and directory operations)
import configparser  # Reads and parses configuration files (e.g., config.ini)
import hashlib  # Provides secure hash algorithms (e.g., SHA256)
import urllib.parse  # Handles URL parsing and encoding of query parameters
import logging  # Records events, errors, and debug information to a log file
import time  # Provides time-related functions (e.g., sleep for retries)
import sys # Provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter
import threading # Provides threading support for running the spinner in the background
import time #  Provides various time-related functions


# 2. Logging configuration
logging.basicConfig(
    filename='audit_script.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 3. Configuration loading and validation
config = configparser.ConfigParser()
config.optionxform = str  # Preserve the case of keys
config_file = 'config.ini'# Update with the actual path to your config.ini
# Example  /Users/first.lastname/Desktop/audit-export-client-v2/config.ini

if not os.path.exists(config_file):
    logging.error("Config file not found. Please ensure 'config.ini' exists.")
    exit(1)

# Check if the file is empty
if os.path.getsize(config_file) == 0:
    logging.error("Config file is empty. Please populate config.ini with the necessary keys.")
    exit(1)

try:
    config.read(config_file)
except configparser.MissingSectionHeaderError as e:
    logging.error(f"Config file is missing a section header: [DEFAULT]")
    logging.error(f"Add [DEFAULT] as the first line of the config file.")
    exit(1)
    
try:
    # Set environment variables from config.ini
    api_token = config['DEFAULT']['API_TOKEN']
    api_token_id = config['DEFAULT']['API_TOKEN_ID']
except KeyError as e:
    logging.error(f"Missing configuration key: {e}")
    exit(1)

if api_token.strip() and api_token_id.strip(): # Check if both tokens are non-empty and log a success message.
    logging.info("API token and token ID loaded from config.ini.")
else:
    logging.error("One or both API token and token ID are empty.")
    exit(1)


# 4. API constants and parameters
# Set up API request parameters
method = "GET"
path = "/audit/api/v1/events"
host = "api.virtru.com"
queryParams = ""

# 5. Utility functions
def generate_date_intervals(start_date, end_date, delta):
    """Generates date intervals for making API requests."""
    current_date = start_date
    while current_date < end_date:
        interval_end = min(current_date + delta, end_date)
        yield (current_date, interval_end)
        current_date = interval_end

def _hash_string(string_to_hash):
    """Build an unseeded hash of a string."""
    return hashlib.sha256(string_to_hash.encode()).hexdigest()

def _build_string_to_hash(headers, path, query, method, body):
    """Construct the string with new lines to sign for authentication."""
    header_string = (
        "content-type:" + headers["content-type"] + "\n" +
        "date:" + headers["date"] + "\n" +
        "host:" + headers["host"] + "\n"
    )
    string_to_hash = (
        method.upper() + "\n" +
        path + "\n" +
        query + "\n" +
        header_string + "\n" +
        "content-type;date;host" + "\n" +
        _hash_string(body)
    )
    return string_to_hash

def make_request_with_retries(url, headers, params, retries=3, backoff_factor=2):
    for attempt in range(retries):
        try:
            response = requests.request(method, url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as he:
            if he.response is not None and he.response.status_code == 403:
                logging.error(f"Received 403 Forbidden on attempt {attempt + 1}. Credentials may be invalid. Not retrying further.")
                raise Exception("Invalid credentials: 403 Forbidden")  # Raise exception immediately
            else:
                logging.warning(f"Attempt {attempt + 1} failed: {he}")
                if attempt < retries - 1:
                    wait_time = backoff_factor ** attempt
                    logging.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logging.error(f"Request failed after {retries} attempts.")
                    raise Exception("Request failed after retries")
        except requests.exceptions.ConnectionError as ce:
            logging.error(f"Lost connection on attempt {attempt + 1}: {ce}")
            if attempt < retries - 1:
                wait_time = backoff_factor ** attempt
                logging.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise Exception("Connection failed after retries")
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                wait_time = backoff_factor ** attempt
                logging.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logging.error(f"Request failed after {retries} attempts.")
                raise Exception("Request failed after retries")


def fetch_data(start_date, end_date):
    """Fetches data for a given interval by making multiple API requests if needed."""
    data = []# Initialize an empty list to store data for each API request within a specific date range.
    # This list will collect the data retrieved from the API response for the given date interval
    # and will be reset for each new interval in the larger loop in the main part of the script.
    nextBookmark = None # Initialize nextBookmark
    max_iterations = 10 # Set a limit to the number of iterations
    current_iteration = 0
    while current_iteration < max_iterations:
        now = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT') # Define 'now' for each request
        bodyHex = sha256("".encode()).hexdigest() # Generate the body hash for each request

        # Build query parameters, adding bookmark if present
        if nextBookmark:
            queryParams_local = f"bookmark={urllib.parse.quote(nextBookmark)}&"
        else:
            queryParams_local = ""
        queryParams_local += f"from={urllib.parse.quote(start_date)}&to={urllib.parse.quote(end_date)}"

        # Prepare the headers for each request
        headers = { 
            'accept': 'application/json',  # Client expects JSON response.
            'date': now,  # Current GMT timestamp for request signing.
            'content-type': 'application/json; charset=utf-8',  # Request body is JSON with UTF-8.
            'host': host,  # Specifies the API host.
            'X-Request-Limit': '1000'  # Limits the API response to a maximum of 1000 records.
        }

        # Generate signature for each request
        string_hash = _build_string_to_hash(
            headers=headers,
            path=path + (f"?{queryParams_local}" if queryParams_local else ""),
            query=queryParams_local,
            method=method,
            body=""
        )

        signature = hmac.new(
            key=api_token.encode(),
            msg=string_hash.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        headers["X-Auth-Signedheaders"] = "content-type;date;host"
        headers["Authorization"] = f"HMAC {api_token_id}:{signature}"

        url = f"https://{host}{path}"
        params = dict(urllib.parse.parse_qsl(queryParams_local))

        response_data = make_request_with_retries(url, headers, params)
        if not response_data:
            logging.error("Failed to fetch data for this interval.")
            break

        data.extend(response_data.get('events', []))
        nextBookmark = response_data.get('bookmarks', {}).get('nextBookmark')
        current_iteration += 1
        if not nextBookmark:
            logging.info("No more bookmarks found. Stopping API requests for this interval.")
            break

    return data
    
def create_directories(base_dir='audit_output'):
    """Creates the required directory structure for output files."""
    json_dir = os.path.join(base_dir, 'json_files')
    csv_dir = os.path.join(base_dir, 'csv_files')
    os.makedirs(json_dir, exist_ok=True)
    os.makedirs(csv_dir, exist_ok=True)

create_directories()

# 6. File writing function (consolidated)
def write_data_to_files(data, date_str, base_dir='audit_output'):
    """
    Writes data to JSON and CSV files.
    Returns the number of files successfully written.
    """
    files_written = 0
    json_file_path = os.path.join(base_dir, 'json_files', f'{date_str}.json')
    csv_file_path = os.path.join(base_dir, 'csv_files', f'{date_str}.csv')
    try:
        if not os.path.exists(json_file_path):
            write_to_json(data, json_file_path)
            logging.info(f"Data for {date_str} written to {json_file_path}")
            files_written += 1
        else:
            logging.info(f"JSON file for {date_str} already exists. Skipping.")

        if not os.path.exists(csv_file_path):
            write_to_csv(data, csv_file_path)
            logging.info(f"Data for {date_str} written to {csv_file_path}")
            files_written += 1
        else:
            logging.info(f"CSV file for {date_str} already exists. Skipping.")
    except Exception as e:
        logging.error(f"Error writing files for {date_str}: {e}")
    return files_written

# 7. Global variables and main execution function
total_files_written = 0
# Define start and end dates and interval length
                #YYYY-MM-DDTHH:MM:SSZ
#start_date_str = '2025-01-01T00:00:00Z' # This can be changed to any starting date
#uncomment the line above to set a specific start date

# Automatically set start_date_str to 30 days before the current UTC time
start_date_dt = datetime.now(timezone.utc) - timedelta(days=30)
start_date_str = start_date_dt.strftime('%Y-%m-%dT%H:%M:%SZ')

# end date is set to the current time
end_date_str = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
start_date = datetime.fromisoformat(start_date_str.rstrip('Z'))
end_date = datetime.fromisoformat(end_date_str.rstrip('Z'))
# Set the interval length for data fetching. Adjust the timedelta value 
# to change the frequency of data retrieval. Uncomment the desired interval.
interval_length = timedelta(days=1)  # Example: 1 day interval
#interval_length = timedelta(hours=6)  # Fetches data in 6-hour chunks
#interval_length = timedelta(days=7)   # Fetches data in 1-week chunks
#interval_length = timedelta(hours=1)  # Fetches data in 1-hour chunks
#interval_length = timedelta(seconds=30)  # Fetches data in 30-second chunks

def main():
    global total_files_written
    for interval_start, interval_end in generate_date_intervals(start_date, end_date, interval_length):
        formatted_start_date = interval_start.isoformat() + 'Z'
        formatted_end_date = interval_end.isoformat() + 'Z'
        interval_data = fetch_data(formatted_start_date, formatted_end_date)
        if interval_data:
            date_str = interval_start.strftime('%Y-%m-%d')
            logging.info(f"Records fetched for {date_str}: {len(interval_data)}")
            total_files_written += write_data_to_files(interval_data, date_str)
        else:
            logging.warning(f"No data received for interval starting {formatted_start_date}")
# Function to display a progress spinner
def spinner():
    symbols = ['|', '/', '-', '\\']
    idx = 0
    while not spinner_done.is_set():
        sys.stdout.write(f"\rScript is running... {symbols[idx % len(symbols)]}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)
    sys.stdout.write("\rScript execution complete!  \n")

# Create an event to signal when the spinner should stop
spinner_done = threading.Event()

if __name__ == '__main__':
    # After loading configuration
    # Validate credentials using make_request_with_retries() before proceeding with data retrieval.
    
    # Then start your spinner thread and main processing...
    # on the console while the script is running.
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    # Execute the main logic of your script
    start_time = datetime.now(timezone.utc)# Log the start time
    logging.info("Script execution started at %s", start_time.strftime("%Y-%m-%d %H:%M:%S %Z"))
    print("\nScript execution started. Please wait...")  # Terminal message
    
    try:
        main()
    except KeyboardInterrupt:
        logging.error("Script execution was interrupted by the user (KeyboardInterrupt).")
    except requests.exceptions.ConnectionError as ce:
        logging.error(f"Lost connection: {ce}")
    except Exception as e:
        logging.error(f"Script encountered an error: {e}")
    else:
        logging.info(f"Total files written: {total_files_written}")
        logging.info("Script ran successfully without any errors")
    finally:
        # Signal the spinner to stop and wait for it to finish
        spinner_done.set()
        spinner_thread.join()
        # Log the end time and total execution time
        end_time = datetime.now(timezone.utc)
        logging.info("Script execution ended at %s", end_time.strftime("%Y-%m-%d %H:%M:%S %Z"))
        execution_time = end_time - start_time
        logging.info("Total execution time: %s", execution_time)

#uncomment the lines below to print the script termination message to the terminal
#print("\n" + "#" * 54)
#print("#" * 54)
#print("#" * 54)
#print("#" + " " * 50 + "#")
#print("#  Audit log generated successfully.                #")
#print("#  For the retrieved data, check the 'audit_output' #")
#print("#  path. The audit data corresponds with the date   #")
#print("#  file.                                            #")
#print("#" + " " * 50 + "#")
#print("#" * 54)
#print("#" * 54)
#print("#" * 54 + "\n")
