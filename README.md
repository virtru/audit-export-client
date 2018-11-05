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
### `--json=<path-to-folder>`

to export audit records to csv, provide a path to a folder
### `--csv=<path-to-folder>`

to export audit records to syslog, provide a host and a port
### `--sysloghost=0.0.0.0 --syslogport=514`

to pull records since the last time the script was run, set the bookmark option
### `--bookmark` or `-b`
you can also provide a `bookmark.ini` file, in  the `.auditexport` directory, which will tell the script where to start pulling records

```ini
#bookmark.ini

[next-page-start-key]
nextpagestartkey=<next-page-start-index>

```

for verbose logging, use the option:
### `--verbose` or `-v`

