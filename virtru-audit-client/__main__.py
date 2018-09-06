import argparse
import utils
from auditClient import AuditClient


parser = argparse.ArgumentParser(prog='VirtruAuditExportClient',
                                 description='Allows the export of audit data from a secure Virtru endpoint.')
parser.add_argument('-i', '--ini',
                    help='Configuration file.  Example: config.ini',
                    dest='configFile',
                    required=True)
parser.add_argument('-s', '--start',
                    help='Start date of query.  Example: -s 2019-01-01',
                    dest='startDate',
                    default='2010-01-01',
                    required=False)
parser.add_argument('-e', '--end',
                    help='End date of query.  Example: -e 2019-02-01',
                    dest='endDate',
                    default='2100-01-01',
                    required=False)
parser.add_argument('--csv',
                    help='CSV output folder.  If defined CSV will be exported',
                    dest='csv',
                    default=None,
                    required=False)
parser.add_argument('--json',
                    help='Json output folder.  If defined Json will be exported.  Example: output/  '
                    '/home/user/json/',
                    dest='json',
                    default=None,
                    required=False)
parser.add_argument('--sysloghost',
                    help='Syslog server.  If defined syslog will be exported',
                    dest='sysloghost',
                    default=None,
                    required=False)
parser.add_argument('--syslogport',
                    help='Syslog port.  If a different port is required.',
                    dest='syslogport',
                    default=None,
                    required=False)

args = parser.parse_args()

config = utils.getConfig(args.configFile)
apiTokenId = config['apiTokenId']
apiTokenSecret = config['apiTokenSecret']
apiHost = config['apiHost']
apiPath = config['apiPath']

bookMark = utils.getNextPageStartKey()
nextPageStartKey = None if not bookMark else bookMark['nextpagestartkey']


queryStart = args.startDate
queryEnd = args.endDate
jsonFolderPath = args.json
csvFolderPath = args.csv
syslogHost = args.sysloghost
syslogPort = args.syslogport


auditClient = AuditClient(apiTokenSecret, apiTokenId,
                          apiHost, apiPath)

req = {
    'method': 'GET',
    'query': {
        'start': queryStart,
        'end': queryEnd
    }
}

if(nextPageStartKey):
    req['query']['nextPageStartKey'] = nextPageStartKey

hasMore = True
iteration = 1

while hasMore:
    records = auditClient.fetchRecords(req)
    if(jsonFolderPath):
        utils.exportToJson(jsonFolderPath, records['docs'])
    if(csvFolderPath):
        utils.exportToCsv(csvFolderPath, records['docs'])
    if(syslogHost is not None and syslogPort is not None):
        utils.exportToSysLog(syslogHost, syslogPort, records['docs'])

    if 'nextPageStartKey' in records:
        req['query']['nextPageStartKey'] = records['nextPageStartKey']
        nextPageStartKey = records['nextPageStartKey']
    else:
        hasMore = False
        if nextPageStartKey:
            utils.saveNextPgeStartKey(nextPageStartKey)
    print('Iteration :' + str(iteration) + '\t\t' +
          "Items: " + str(len(records['docs'])))
    iteration += 1
