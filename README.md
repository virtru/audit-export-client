# virtru-audit-export-client

Python based Virtru Audit Export Client.

## Getting started
install pipenv using `brew`

```bash 
brew install pipenv
````

install package dependencies

```bash
pipenv install
```

## Usage

run the script using:

```bash
pipenv run python virtru-audit-client
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

to export audit records to json, provide a path to a folder

### `--json=<path-to-folder>`

to export audit records to csv, provide a path to a folder

### `--csv=<path-to-folder>`

to export audit records to syslog, provide a host and a port

### `--sysloghost=0.0.0.0 --syslogport=514`

you can also provide a `bookmark.ini` file which will tell the script where to start pulling records

```ini
#bookmark.ini

[next-page-start-key]
nextpagestartkey=<next-page-start-index>

```