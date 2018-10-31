import pytest
import base64
import iso8601
from string import Template
from auditexport import utils, cli
from auditexport.auditclient import AuditClient
from unittest.mock import Mock, call
from collections import namedtuple

SOME_ID = 'some-id'
SOME_SECRET = 'some-secret'
SOME_HOST = 'audit.virtru.com'
SOME_PATH = '/api/messages'
SOME_RECORD_ID_1 = 'some-record-id'
BOOKMARK = {
    'nextpagestartkey': 'some-next-page-key'
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
        'docs': [
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
    'Args', 'startDate endDate csv json sysloghost syslogport useBookMark')


@pytest.fixture
def mock_utils():
    mock_utils = Mock(spec=utils)
    mock_utils.getConfig.return_value = SOME_CONFIG
    mock_utils.getNextPageStartKey.return_value = BOOKMARK
    mock_utils.saveNextPageStartKey.return_value = None
    mock_utils.exportToJson.return_value = None
    mock_utils.exportToCsv.return_value = None
    mock_utils.exportToSysLog.return_value = None
    return mock_utils


def test_process_succeeds_no_options(mock_utils, mock_audit_client):
    args = MockArgs(startDate='2017',
                    endDate='2018', csv=None, json=None, sysloghost=None, syslogport=None, useBookMark=False)
    cli.process(args, mock_audit_client, mock_utils)
    mock_utils.getNextPageStartKey.assert_called_with()
    mock_utils.saveNextPageStartKey.assert_not_called()
    mock_utils.exportToJson.assert_not_called()
    mock_utils.exportToCsv.assert_not_called()
    mock_utils.exportToSysLog.assert_not_called()
    mock_audit_client.fetchRecords.assert_called_with({
        'method': 'GET',
        'query': {
            'start': '2017',
            'end': '2018'
        }
    })


def test_process_succeeds_with_options(mock_utils, mock_audit_client, mock_response):
    args = MockArgs(startDate='2017',
                    endDate='2018', csv='some-csv', json='some-json', sysloghost='some-syslog', syslogport='some-port', useBookMark='some-bmk')
    cli.process(args, mock_audit_client, mock_utils)
    mock_utils.getNextPageStartKey.assert_called_with()
    mock_utils.saveNextPageStartKey.assert_called_with(SOME_RECORD_ID_1)
    mock_utils.exportToJson.assert_called_with(
        'some-json', mock_response['docs'])
    mock_utils.exportToCsv.assert_called_with(
        'some-csv', mock_response['docs'])
    mock_utils.exportToSysLog.assert_called_with(
        'some-syslog', 'some-port', mock_response['docs'])


def test_process_with_bookMark(mock_audit_client, mock_utils):
    mock_utils.getNextPageStartKey.return_value = BOOKMARK
    args = MockArgs(startDate='2017',
                    endDate='2018', csv=None, json=None, sysloghost=None, syslogport=None, useBookMark=True)
    cli.process(args, mock_audit_client, mock_utils)
    mock_audit_client.fetchRecords.assert_called_with({
        'method': 'GET',
        'query': {
            'start': '2017',
            'end': '2018',
            'nextPageStartKey': BOOKMARK['nextpagestartkey']
        }
    })


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
            'nextPageStartKey': SOME_NEXT_PAGE_KEY
        }
    })]
    mock_response_2 = mock_response
    mock_response_1 = dict(mock_response)
    mock_response_1['nextPageStartKey'] = SOME_NEXT_PAGE_KEY
    mock_audit_client.fetchRecords.side_effect = [
        mock_response_1, mock_response_2]

    args = MockArgs(startDate='2017',
                    endDate='2018', csv=None, json=None, sysloghost=None, syslogport=None, useBookMark=False)
    cli.process(args, mock_audit_client, mock_utils)
    assert mock_audit_client.fetchRecords.call_count == 2
    assert mock_utils.saveNextPageStartKey.call_count == 0
    # mock_audit_client.fetchRecords.assert_has_calls(
    #     EXPECTED_CALLS, any_order=True)


def test_process_throws_on_invalid_date(mock_audit_client, mock_utils):
    args = MockArgs(startDate='201ask',
                    endDate='adlk2', csv=None, json=None, sysloghost=None, syslogport=None, useBookMark=True)
    with pytest.raises(iso8601.ParseError):
        cli.process(args, mock_audit_client, mock_utils)
