import pytest
import base64
import requests
import sys
from unittest.mock import Mock
from auditclient import errors
from auditclient.audit_client import AuditClient


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
    emptyResponse = {
        'doc': []
    }

    def create_mock(response=emptyResponse, status_code=200):
        response = emptyResponse if request.param is None else request.param
        mock = Mock(spec=requests)
        mockResponse = Mock(spec=requests.Response)
        mockResponse.status_code = status_code
        mockResponse.json.return_value = mock.get.return_value = response
        mock.get.return_vale = None
        mock.get.return_value = mockResponse
        return mock
    return create_mock(request.param[0], request.param[1])


def test_generateQueryParams(some_audit_client, some_req):
    query = some_req['query']
    keys = ['start', 'end']
    toTest = some_audit_client._generateQueryParams(query, keys)
    assert toTest == 'start=2000end=2018'


response = {
    'doc': [],
    'nextPageStartKey': 'some-key'
}


@pytest.mark.parametrize('expected_exception', [errors.ClientConnectionError])
@pytest.mark.parametrize('mock_requests', [(response, 400)], indirect=True)
def test_fetch(monkeypatch, some_audit_client, some_req, mock_requests, expected_exception):
    """ Test to make sure errors are thrown """

    monkeypatch.setattr('auditclient.audit_client.requests', mock_requests)
    with pytest.raises(expected_exception):
        some_audit_client.fetchRecords(some_req)
