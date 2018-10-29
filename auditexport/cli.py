import argparse
import logging
import sys
import iso8601
from . import utils
from .auditclient import AuditClient


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
    parser.add_argument('--bookmark', '-b',
                        help='Start from last bookmark',
                        dest='useBookMark',
                        default=False,
                        required=False,
                        action='store_true')

    args = parser.parse_args()

    process(args)


def process(args):
    # Get config information from config.ini file
    config = utils.getConfig(args.configFile)
    apiTokenId = config['apiTokenId']
    apiTokenSecret = config['apiTokenSecret']
    apiHost = config['apiHost']
    apiPath = config['apiPath']

    bookMark = utils.getNextPageStartKey()
    nextPageStartKey = None if not bookMark else bookMark['nextpagestartkey']

    queryStart = args.startDate
    queryEnd = args.endDate

    __validateDates(queryStart, queryEnd)

    jsonFolderPath = args.json
    csvFolderPath = args.csv
    syslogHost = args.sysloghost
    syslogPort = args.syslogport
    useBookMark = args.useBookMark

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

    auditclient = AuditClient(apiTokenSecret, apiTokenId, apiHost, apiPath)

    while hasMore:
        records = auditclient.fetchRecords(req)
        if(jsonFolderPath and records['docs']):
            utils.exportToJson(jsonFolderPath, records['docs'])
        if(csvFolderPath and records['docs']):
            utils.exportToCsv(csvFolderPath, records['docs'])
        if(syslogHost is not None and syslogPort is not None and records['docs']):
            utils.exportToSysLog(syslogHost, syslogPort, records['docs'])

        if 'nextPageStartKey' in records:
            nextPageStartKey = records['nextPageStartKey']
            req['query']['nextPageStartKey'] = nextPageStartKey
        else:
            hasMore = False
            if records['docs']:
                nextPageStartKey = records['docs'][-1]['recordId']
        utils.saveNextPageStartKey(nextPageStartKey)
        print('Iteration :' + str(iteration) + '\t\t' + 'Items: ' +
              str(len(records['docs'])) + '\t\t' + 'NextPageStartKey: ' + str(nextPageStartKey))
        iteration += 1


def __validateDates(start, end):
    """ Validate dates are correct iso8601 format"""
    try:
        iso8601.parse_date(start)
        iso8601.parse_date(end)
    except ParseError as e:
        logging.error(
            'Error parsing start/end. Make sure date are valid ISO8601 format')
        sys.exit(-1)


if __name__ == "__main__":
    main()
