import pytest
import base64
import requests
import sys
import jwt
import time
from unittest.mock import Mock
from auditexport.auditclient.errors import InvalidCredentialsError, ClientConnectionError
from auditexport.auditclient import AuditClient


@pytest.fixture
def some_audit_client():
    return AuditClient(base64.b64encode(b'somesecret'), 'someId', 'someHost', 'someApiPath')


@pytest.fixture
def some_req():
    return {
        'method': 'GET',
        'query': {
            'start': '2000',
            'end': '2018'
        }
    }


@pytest.fixture
def mock_requests(request):
    def create_mock(response, status_code=200):
        mock = Mock(spec=requests)
        mockResponse = Mock(spec=requests.Response)
        mockResponse.status_code = status_code
        mockResponse.json.return_value = response
        mock.get.return_value = mockResponse
        return mock
    return create_mock(request.param[0], request.param[1])


def test_generateQueryParams(some_audit_client, some_req):
    query = some_req['query']
    keys = ['start', 'end']
    toTest = some_audit_client._generateQueryParams(query, keys)
    assert toTest == 'start=2000end=2018'


error_responses = [
    ((None, 401), InvalidCredentialsError),
    ((None, 400), ClientConnectionError),
    ((None, 500), ClientConnectionError),
    ((None, 403), InvalidCredentialsError)
]


@pytest.mark.parametrize('mock_requests, expected_exception', error_responses, indirect=['mock_requests'])
def test_fetch_throws_errors(monkeypatch, some_audit_client, some_req, mock_requests, expected_exception):
    """ Test to make sure errors are thrown """
    monkeypatch.setattr(
        'auditexport.auditclient.auditclient.requests', mock_requests)
    with pytest.raises(expected_exception):
        some_audit_client.fetchRecords(some_req)


def test_generateVjwtString_throws(some_req):
    SOME_INVALID_CLIENT = AuditClient('invalid-secret', 'some-id')
    with pytest.raises(InvalidCredentialsError):
        SOME_INVALID_CLIENT._generateVjwtString(some_req)
