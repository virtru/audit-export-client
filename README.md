# Audit Export Client v2 - Installation

Python client for pulling audit data from the Virtru audit API.

## Getting started
## This application currently works on MacOS

Before running the script, ensure that your system meets the following requirements:

## Linux
This requires **`python 3.5.0`** or higher

Environment Update:

```bash 
sudo apt update && sudo apt upgrade
````
```bash  
sudo apt get upgrade openssl
````
```bash
sudo aptget install python3
````
```bash
curl https://bootstrap.pypa.io/getpip.py o getpip.py
````
```bash
python3 m pip version
````
```bash
/usr/bin/python3 m pip install requests
````
```bash
pip3 install pandas
```
## MacOS
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
```
## Install Pip: Follow the same steps as in Linux.
 
# Installation Guide
### 1.	Create Directories:
```bash
mkdir /var/virtru
````
```bash
mkdir /var/virtru/audit
````
### 2.	Clone the Repository:
```bash
cd /var/virtru/audit
````
```bash
git clone https://github.com/virtru/virtru-audit-export-client.git
````
```bash
cd virtru-audit-export-client/
````
### 3.	 Configuration
### 1.	Edit Config File: 
```bash
vim config.ini
````
### 2.	Enter the HMAC token and secret.
### 3.	Update with the actual path to your 'config.ini'.=

## Running the Script
## Execute the script using one of the following commands based on your system's configuration:
## Change the starting date in the auditclient.py:
```bash
python3 /var/virtru/audit/auditexportclientv2/auditclient.py
````
```bash
/usr/bin/python3 /path/to/your/script/auditclient.py
````
## Viewing the Output
## JSON Output: Navigate to 
```bash
/var/virtru/audit/auditexportclientv2/audit_output/cd output.json
````
## CSV Output: Navigate to 
```bash
/var/virtru/audit/auditexportclientv2/audit_output/output.csv
````
## Use the ‘cat' command to view the file, e.g., 'cat filename.csv' or 'cat filename.json’
