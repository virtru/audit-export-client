import argparse
import logging
import sys
import iso8601
# from . import utils
from .auditclient import AuditClient, utils

logger = logging.getLogger(__name__)


def main():
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
                        default='514',
                        required=False)
    parser.add_argument('-b', '--bookmark',
                        help='Start from last bookmark',
                        dest='useBookMark',
                        default=False,
                        required=False,
                        action='store_true')
    parser.add_argument('-v', '--verbose',
                        help='Verbose option',
                        dest='verbose',
                        default=False,
                        required=False,
                        action='store_true')

    # Get args from config parser
    args = parser.parse_args()

    # Set Log level
    loglevel = logging.DEBUG if args.verbose is True else logging.ERROR
    logger.parent.handlers[0].setLevel(loglevel)

    logger.debug('debugging.....')

    # Get config information from config.ini file
    logger.debug('retriving info from config.ini....')
    config = utils.getConfig(args.configFile)
    apiTokenId = config['apiTokenId']
    apiTokenSecret = config['apiTokenSecret']
    apiHost = config['apiHost']
    apiPath = config['apiPath']

    # Initialize auditclient
    auditclient = AuditClient(apiTokenSecret, apiTokenId, apiHost, apiPath)

    # Begin Processing
    # try:
    logger.debug('begin processing......')
    process(args, auditclient, utils)
    # except ParseError as e:
    #     logging.error(
    #         'Error parsing start/end. Make sure date are valid ISO8601 format')
    #     sys.exit(-1)


def process(args, auditclient, utils):

    bookMark = utils.getNextPageStartKey()
    nextPageStartKey = None if not bookMark else bookMark['nextpagestartkey']

    queryStart = args.startDate
    queryEnd = args.endDate

    # Check dates are in valid IS08601 format
    iso8601.parse_date(queryStart)
    iso8601.parse_date(queryEnd)

    jsonFolderPath = args.json
    csvFolderPath = args.csv
    syslogHost = args.sysloghost
    syslogPort = args.syslogport
    useBookMark = args.useBookMark

    # Syslog logger
    syslogger = None

    if syslogHost is not None:
        syslogger = logging.getLogger('virtru-export')
        syslogger.setLevel(logging.WARNING)

    req = {
        'method': 'GET',
        'query': {
            'start': queryStart,
            'end': queryEnd
        }
    }

    if(nextPageStartKey and useBookMark):
        req['query']['nextPageStartKey'] = nextPageStartKey

    hasMore = True
    iteration = 1

    logger.debug('fetching audit records....')
    while hasMore:
        records = auditclient.fetchRecords(req)
        if(jsonFolderPath and records['docs']):
            utils.exportToJson(jsonFolderPath, records['docs'])
        if(csvFolderPath and records['docs']):
            utils.exportToCsv(csvFolderPath, records['docs'])
        if(syslogHost is not None and records['docs']):
            utils.exportToSysLog(syslogHost, syslogPort,
                                 syslogger, records['docs'])

        if 'nextPageStartKey' in records:
            nextPageStartKey = records['nextPageStartKey']
            req['query']['nextPageStartKey'] = nextPageStartKey
        else:
            hasMore = False
            if records['docs']:
                nextPageStartKey = records['docs'][-1]['recordId']

        if(useBookMark):
            utils.saveNextPageStartKey(nextPageStartKey)

        print('Iteration :' + str(iteration) + '\t\t' + 'Items: ' +
              str(len(records['docs'])) + '\t\t' + 'NextPageStartKey: ' + str(nextPageStartKey))
        iteration += 1
