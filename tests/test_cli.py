import pytest
import base64
import iso8601
import copy
from string import Template
from auditexport import utils, cli
from auditexport.auditclient import AuditClient
from unittest.mock import Mock, call, MagicMock
from collections import namedtuple

SOME_ID = 'some-id'
SOME_SECRET = 'some-secret'
SOME_HOST = 'audit.virtru.com'
SOME_PATH = '/api/messages'
SOME_RECORD_ID_1 = 'some-record-id'
CURSOR = {
    'nextPageCursor': 'some-next-page-key',
    'lastRecordSaved': 'some-record-id'
}

SOME_CONFIG = {
    'apiTokenSecret': SOME_SECRET,
    'apiTokenId': SOME_ID,
    'apiHost': SOME_HOST,
    'apiPath': SOME_PATH
}


@pytest.fixture
def mock_response():
    return {
        'cursor': {},
        'data': [
            {
                'recordId': SOME_RECORD_ID_1
            }
        ]
    }


@pytest.fixture
def mock_audit_client(mock_response):
    mock = Mock(spec=AuditClient)
    mock.fetchRecords.return_value = mock_response
    return mock


MockArgs = namedtuple(
    'Args', 'startDate endDate csv json sysloghost syslogport useCursor limit')


@pytest.fixture
def mock_utils():
    mock_utils = MagicMock(spec=utils)
    mock_utils.getConfig.return_value = SOME_CONFIG
    mock_utils.checkRecords.return_value = [{'recordId': SOME_RECORD_ID_1}]
    mock_utils.getnextPageCursor.return_value = CURSOR
    mock_utils.saveNextPageCursor.return_value = None
    mock_utils.exportToJson.return_value = None
    mock_utils.exportToCsv.return_value = None
    mock_utils.exportToSysLog.return_value = None
    mock_utils.configSysLogger.return_value = 'some-logger'
    return mock_utils

@pytest.fixture
def mock_utiles_checkrecords():
    mock_utils = MagicMock(spec=utils)
    mock_utils.getnextPageCursor.return_value = CURSOR
    mock_utils.getnextPageCursor.checkRecords = []
    mock_utils.saveNextPageCursor.return_value = None
    return mock_utils


def test_process_succeeds_no_options(mock_utils, mock_audit_client):
    args = MockArgs(startDate='2017',
                    endDate='2018', csv=None, json=None, sysloghost=None, syslogport=None, useCursor=False, limit=100)
    cli.process(args, mock_audit_client, mock_utils)
    mock_utils.getnextPageCursor.assert_called_with()
    mock_utils.saveNextPageCursor.assert_not_called()
    mock_utils.exportToJson.assert_not_called()
    mock_utils.exportToCsv.assert_not_called()
    mock_utils.exportToSysLog.assert_not_called()
    mock_audit_client.fetchRecords.assert_called_with({
        'method': 'GET',
        'query': {
            'start': '2017',
            'end': '2018',
            'limit': 100,
            'sort': 'timestamp:asc'
        }
    })


def test_process_succeeds_with_options(mock_utils, mock_audit_client, mock_response):
    args = MockArgs(startDate='2017', limit=150,
                    endDate='2018', csv='some-csv', json='some-json', sysloghost='some-syslog', syslogport='514', useCursor='some-bmk')
    cli.process(args, mock_audit_client, mock_utils)
    mock_utils.checkRecords.assert_called_with([{'recordId': 'some-record-id'}], 'some-record-id')
    mock_utils.getnextPageCursor.assert_called_with()
    mock_utils.saveNextPageCursor.assert_called_with(CURSOR['nextPageCursor'], SOME_RECORD_ID_1)
    mock_utils.exportToJson.assert_called_with(
        'some-json', mock_response['data'])
    mock_utils.exportToCsv.assert_called_with(
        'some-csv', mock_response['data'], {})
    mock_utils.exportToSysLog.assert_called_with(
        'some-syslog', '514', mock_utils.configSysLogger('some-syslog', '514'), mock_response['data'])


def test_process_with_cursor(mock_audit_client, mock_utils):
    mock_utils.getnextPageCursor.return_value = CURSOR
    args = MockArgs(startDate='2017', limit=200,
                    endDate='2018', csv=None, json=None, sysloghost=None, syslogport=None, useCursor=True)
    cli.process(args, mock_audit_client, mock_utils)
    mock_audit_client.fetchRecords.assert_called_with({
        'method': 'GET',
        'query': {
            'start': '2017',
            'end': '2018',
            'sort': 'timestamp:asc',
            'cursor': CURSOR['nextPageCursor'],
            'limit': 200
        }
    })

def test_process_with_no_new_records_to_save(mock_utiles_checkrecords, mock_audit_client):
    args = MockArgs(startDate='2017',
                    endDate='2018', csv=None, json=None, sysloghost=None, syslogport=None, useCursor=False, limit=100)
    cli.process(args, mock_audit_client, mock_utiles_checkrecords)
    mock_utiles_checkrecords.saveNextPageCursor.assert_not_called()
    assert mock_audit_client.fetchRecords.call_count == 1


def test_process_with_next_pagesStartkey(mock_audit_client, mock_utils, mock_response):
    mock_audit_client.fetchRecords.return_value = None
    SOME_NEXT_PAGE_KEY = 'some-start-key'
    EXPECTED_CALLS = [call({
        'method': 'GET',
        'query': {
            'start': '2017',
            'end': '2018'
        }
    }), call({
        'method': 'GET',
        'query': {
            'start': '2017',
            'end': '2018',
            'cursor': SOME_NEXT_PAGE_KEY
        }
    })]
    mock_response_2 = mock_response
    mock_response_1 = copy.deepcopy(mock_response)
    mock_response_1['cursor']['after'] = SOME_NEXT_PAGE_KEY
    mock_audit_client.fetchRecords.side_effect = [
        mock_response_1, mock_response_2]

    args = MockArgs(startDate='2017', limit=100,
                    endDate='2018', csv=None, json=None, sysloghost=None, syslogport=None, useCursor=False)
    cli.process(args, mock_audit_client, mock_utils)
    assert mock_audit_client.fetchRecords.call_count == 2
    assert mock_utils.saveNextPageCursor.call_count == 0
    # mock_audit_client.fetchRecords.assert_has_calls(
    #     EXPECTED_CALLS, any_order=True)


def test_process_throws_on_invalid_date(mock_audit_client, mock_utils):
    args = MockArgs(startDate='201ask', limit=False,
                    endDate='adlk2', csv=None, json=None, sysloghost=None, syslogport=None, useCursor=True)
    with pytest.raises(iso8601.ParseError):
        cli.process(args, mock_audit_client, mock_utils)
