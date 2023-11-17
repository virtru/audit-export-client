# Virtru Audit Export Client v2

Python client for pulling audit data from the Virtru audit API.

## Getting started
## This application currently works on MacOS
This requires **`python 3.5.0`** or higher

```bash 
brew upgrade
````
```bash 
brew update
````
```bash 
brew upgrade openssl
````
```bash 
brew install python
````
```bash 
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
````
```bash 
python3 -m pip --version
````
```bash 
/usr/bin/python3 -m pip install requests
````
```bash 
pip3 install pandas
````

you must provide a `.ini` file with the following configuration:
# Current config
```ini
[DEFAULT]
apiTokenId=<apiTokenId>
apiTokenSecret=<apiTokenSecret>
```

you must provide the `auditclient.py` file with the following configuration:
# Current auditclient.py
```auditclient.py 
# Read configuration file
config = configparser.ConfigParser() 

# current config, udate with the path if an error occurs
config.read('config.ini')  
# Update with the actual path to your config.ini
config.read('/Users/first.lastname/Desktop/Audit_V2/config.ini') 

# Set environment variables from config
api_token = config['DEFAULT']['API_TOKEN']
api_token_id = config['DEFAULT']['API_TOKEN_ID']

method = "GET"
path = "/audit/api/v1/events"
queryParams = ""
host = "api.virtru.com"
```
Run the script using:

```bash 
/opt/homebrew/bin/python3 /Users/first.lastname/Desktop/auditclient.py
````
## Options
## 1
the start/end dates are hard coded to pull records automatically.  **`NOTE:`** the end date is current date and time; the start date is now - 365 days **`ISO 8601`** format. Currently default to `start=2010-01-01` `end=2100-01-01`:

## 2
uncomment the date prompt to specify start/end dates for pulling records.  **`NOTE:`** all dates must be in a valid **`ISO 8601`** format. Currently default to `start=2010-01-01` `end=2100-01-01`:


### `-See the 'audit_output' path for the audit file`

the output directory contain the human readable files
### `--csv`

the output directory contain the machine readable files
### `--json`