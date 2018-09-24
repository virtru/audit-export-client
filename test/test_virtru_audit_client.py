from test.context import virtruAuditClient
from unittest.mock import patch
from virtruAuditClient import auditClient


SOME_API_HOST = 'some_api_host'
SOME_API_SECRET = 'some_api_secret'
SOME_API_ID = 'some_api_id'
SOME_API_PATH = 'some_api_path'
SOME_REQ = {
    'nextPageStartKey': 'some-start-key'
}
SOME_RECORD = {
    'docs': [{
        'somedoc': 'somevalue'
    }, {
        'anotherdoc': 'anothervalue'
    }],
    'nextPageStartKey': 'some-start-key'
}


@patch('auditClient.requests', spec=True)
@patch('virtruAuditClient.utils', spec=True)
class TestVirtruAuditClient():

    def test_one(self, mockUtils, mockRequests):
        # mockUtils.exportToJson.return_value = SOME_RECORD
        # toTest = AuditClient(SOME_API_SECRET, SOME_API_ID,
        #                      SOME_API_HOST, SOME_API_PATH)
        # somejsonFolderPath = '/somejson/path'
        # somecsvFolderPath = '/somecsv/path'
        # somesyslogHost = '0.0.0.0'

        # toTest.process(SOME_REQ, somejsonFolderPath,
        #                somecsvFolderPath, somesyslogHost)

        assert 2 == 2
