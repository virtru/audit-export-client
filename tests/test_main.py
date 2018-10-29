import pytest
from string import Template
from auditexport import cli
from unittest.mock import Mock
from collections import namedtuple


MockArgs = namedtuple('Args', 'configFile')


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
    fakeConfigFile.write(fakeConfig)
    return fakeConfigFile


@pytest.mark.parametrize('mock_config_file', [('id', 'secret')], indirect=['mock_config_file'])
def test_main_succeeds(monkeypatch, mock_config_file):
    args = MockArgs(configFile='tst')
    cli.process(args)
    pass
