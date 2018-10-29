import pytest
from string import Template
from auditexport import utils


INVALID_CONFIG = """
[ApiInfo]
apiTokenId=tokenId
apiHost=audit.virtru.com
apiPath=/api/messages
"""

EMPTY_CONFIG = """
[ApiInfo]
apiTokenId=tokenId
apiTokenSecret=tokenSecret
apiHost=audit.virtru.com
apiPath=/api/messages
"""


def mock_config(tokenId='', tokenSecret=''):
    return Template('[ApiInfo]\n' +
                    'apiTokenId=$tokenId\n' +
                    'apiTokenSecret=$tokenSecret\n' +
                    'apiHost=audit.virtru.com\n' +
                    'apiPath=/api/messages\n').substitute(tokenId=tokenId, tokenSecret=tokenSecret)


def test_getConfig_no_file():
    with pytest.raises(FileNotFoundError):
        utils.getConfig('invalidPath')


def test_getConfig_throws(tmpdir):
    fakeConfigFile = tmpdir.mkdir('sub').join('config.ini')
    fakeConfigFile.write(INVALID_CONFIG)
    with pytest.raises(utils.InvalidConfigError):
        utils.getConfig(str(fakeConfigFile))


def test_getConfig_succeeds(tmpdir):
    someid = 'someid'
    somesecret = 'somesecret'

    fakeConfigFile = tmpdir.mkdir('sub').join('config.ini')
    fakeConfig = mock_config(someid, somesecret)
    fakeConfigFile.write(fakeConfig)
    config = utils.getConfig(str(fakeConfigFile))
    assert config == {
        'apiTokenSecret': somesecret,
        'apiTokenId': someid,
        'apiHost': 'audit.virtru.com',
        'apiPath': '/api/messages'
    }


def test_getBooMark_returns_none(tmpdir):
    pass
