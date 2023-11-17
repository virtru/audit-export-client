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


# Update with the actual path to your config.ini
# example:
config.read('/Users/first.lastname/Desktop/Audit_V2/config.ini') 


Run the script using:
/opt/homebrew/bin/python3 /Users/first.lastname/Desktop/auditclient.py


you must provide a `.ini` file with the following configuration:

```ini
[ApiInfo]
apiTokenId=<apiTokenId>
apiTokenSecret=<apiTokenSecret>
apiHost="api.virtru.com"
apiPath="/audit/api/v1/events"
```

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