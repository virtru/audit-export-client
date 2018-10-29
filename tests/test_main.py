import pytest
import base64
import requests
from string import Template
from auditexport import cli
from unittest.mock import Mock
from collections import namedtuple

RESPONSE = {
    'docs': [
        {
            'recordId': 'some-record-id'
        }
    ]
}

MockArgs = namedtuple(
    'Args', 'configFile startDate endDate csv json sysloghost syslogport useBookMark')


def mock_config(tokenId='', tokenSecret=''):
    return Template('[ApiInfo]\n' +
                    'apiTokenId=$tokenId\n' +
                    'apiTokenSecret=$tokenSecret\n' +
                    'apiHost=audit.virtru.com\n' +
                    'apiPath=/api/messages\n').substitute(tokenId=tokenId, tokenSecret=tokenSecret)


@pytest.fixture
def mock_config_file(request, tmpdir):
    tokenId = request.param[0]
    tokenSecret = request.param[1]
    fakeConfigFile = tmpdir.mkdir('sub').join('config.ini')
    fakeConfig = mock_config(tokenId, tokenSecret)
    print(fakeConfig)
    fakeConfigFile.write(fakeConfig)
    return fakeConfigFile


@pytest.fixture
def mock_requests_succeeds():
    def create_mock(response, status_code=200):
        mock = Mock(spec=requests)
        mockResponse = Mock(spec=requests.Response)
        mockResponse.status_code = status_code
        mockResponse.json.return_value = response
        mock.get.return_value = mockResponse
        return mock
    return create_mock(RESPONSE)


@pytest.mark.parametrize('mock_config_file', [('id', 'c29tZS1zZWNyZXQ=')], indirect=['mock_config_file'])
def test_main_succeeds(monkeypatch, mock_config_file, tmpdir, mock_requests_succeeds):
    monkeypatch.setattr(
        'auditexport.auditclient.audit_client.requests', mock_requests_succeeds)
    args = MockArgs(configFile=str(mock_config_file), startDate='2017',
                    endDate='2018', csv=None, json=None, sysloghost=None, syslogport=None, useBookMark=False)
    cli.process(args)
    pass
