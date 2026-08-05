# Virtru Audit Export Client

Python client for exporting audit event data from the [Virtru Audit API](https://github.com/virtru-corp/audit-api). Fetches events in configurable date intervals and writes them to both JSON and CSV files.

## Prerequisites

- Python 3.7 or higher
- `requests` library

Install the dependency:

```bash
pip3 install requests
```

## Configuration

Create a `config.ini` file in the project directory with your API credentials:

```ini
[DEFAULT]
API_TOKEN=<your-api-token>
API_TOKEN_ID=<your-token-id>@tokens.virtru.com
```

Your API token and token ID are provided by Virtru. The client authenticates using HMAC-signed requests against `api.virtru.com`.

### Optional config settings

| Key | Description | Default |
|-----|-------------|---------|
| `OUTPUT_DIR` | Directory for output files | `audit_output` |

## Usage

Run the script from the project directory:

```bash
python3 auditclient.py
```

### CLI options

| Option | Description | Default |
|--------|-------------|---------|
| `--output-dir`, `-o` | Directory to write audit files | Value from `config.ini`, or `audit_output` |

Example with a custom output directory:

```bash
python3 auditclient.py --output-dir /path/to/output
```

## How it works

The client fetches audit events from the Virtru Audit API (`/audit/api/v1/events`) over a date range, broken into configurable intervals (default: 1 day). It paginates through results using bookmarks and writes each interval's data to both JSON and CSV files.

### Date range

By default, the start date is `2026-01-01` and the end date is the current UTC time. To change the start date or interval length, edit the values in `auditclient.py`.

### Output

Files are written to subdirectories under the output directory:

```
audit_output/
  json_files/
    2026-01-01.json
    2026-01-02.json
    ...
  csv_files/
    2026-01-01.csv
    2026-01-02.csv
    ...
```

If a file for a given date already exists, it is skipped.

### CSV fields

The CSV output flattens each audit event into these columns:

`id`, `object_type`, `object_id`, `object_name`, `action_type`, `action_result`, `owner_id`, `owner_orgId`, `actor_id`, `client_info_userAgent`, `client_info_platform`, `client_info_requestIp`, `event_meta_data_type`, `event_meta_data_record_id`, `event_meta_data_record_type`, `timestamp`

## Event data model

Each exported event contains an object, action, actor, owner, and client info. Below are the possible values for the key fields.

### Object types

| Type | Description |
|------|-------------|
| `data_object` | Emails or files |
| `user_object` | User activity — account creation, deletion, settings changes |
| `organization_object` | Organization creation or settings changes |
| `rule_object` | DLP rules — creation, deletion, modifications, violations |
| `organizational_unit_object` | Organizational units or user group changes |
| `auth_session_object` | Authentication events (OIDC logins/logouts) |
| `key_object` / `token_object` | CSE and organizational key lifecycle (creation, deletion, updates) |
| `entity_object` | License invitations and related actions |
| `attribute_object` | Attribute-related events |

### Action types

| Type | Description |
|------|-------------|
| `create` | A new object was created |
| `read` | A user viewed or accessed content |
| `update` | An existing object was modified |
| `delete` | An object was removed |
| `triggered` | A DLP rule was triggered or violated |
| `revoke` | A policy, HMAC token, or key was invalidated |
| `wrap` / `unwrap` / `rewrap` | Cryptographic operations (CSE) |
| `digest` / `key_decrypt` / `key_sign` | Additional cryptographic operations |
| `private_key_wrap` / `privileged_wrap` / `system_wrap` | Key wrapping operations |

### Action results

| Result | Description |
|--------|-------------|
| `success` | Action completed successfully |
| `error` | Action failed (e.g., insufficient permissions) |
| `encrypt` | DLP rule enforced encryption |
| `block` | DLP rule prevented sending |
| `override` | User bypassed a DLP warning |
| `cancel` | User cancelled after a DLP warning |
| `ignore` | Action was ignored |
| `failure` | Action failed |

## API Documentation

Full API documentation is available via the Swagger spec in the [audit-api repo](https://github.com/virtru-corp/audit-api/blob/main/docs/swagger.yaml).

The API also supports query filters beyond what this client uses, including `objectType`, `actorId`, `actionType`, `actionResult`, `ownerId`, `objectId`, `ipAddress`, `search`, and `sort`. See the Swagger spec for details.

## Version

Current version: **2.1.0** (defined in `version.py`)
