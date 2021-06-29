[![Build Status](https://badge.buildkite.com/166e874e86a6ffde87aa00021d68367e89d5d08a206d1f5cbf.svg)](https://buildkite.com/virtru/audit-export-client)

# Virtru Audit Export Client

Python client for pulling audit data from the Virtru audit API.

## Getting started
This requires **`python 3.5.0`** or higher

install pipenv using `brew`

```bash 
brew install pipenv
````

install package dependencies

```bash
pipenv install --three
```

## Usage

run the script using:

```bash
pipenv run start
```

you must provide a `.ini` file with the following configuration:

```ini
[ApiInfo]
apiTokenId=<apiTokenId>
apiTokenSecret=<apiTokenSecret>
apiHost=audit.virtru.com
apiPath=/api/messages
```

## Options
to specify start/end dates for pulling records.  **`NOTE:`** all dates must be in a valid **`ISO 8601`** format. Currently default to `start=2010-01-01` `end=2100-01-01`:
### `--start=<start-date>`  `--end=<end-date>`

to export audit records to json, provide a path to a folder
### `--safe-filename`

to use a system safe filename. Alphanumeric and hyphens.
### `--json=<path-to-folder>`

to export audit records to csv, provide a path to a folder
### `--csv=<path-to-folder>`

to export audit records to syslog, provide a host and a port
### `--sysloghost=0.0.0.0 --syslogport=514`

to pull records since the last time the script was run, set the cursor option
### `--cursor` or `-c`
you can also provide a `cursor.ini` file, in  the `.auditexport` directory, which will tell the script where to start pulling records

```ini
#cursor.ini

[next-page-start-key]
nextpagecursor=<next-page-cursor>
lastrecordsaved=<recordId>

```

for verbose logging, use the option:
### `--verbose` or `-v`

