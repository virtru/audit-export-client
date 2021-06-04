import argparse, logging, iso8601
from . import utils
from .auditclient import AuditClient

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
    parser.add_argument('--safe-filename',
                        help='Use a system safe filename. Alphanumeric and hyphens.',
                        dest='safeFilename',
                        action='store_true',
                        default=False,
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
    parser.add_argument('-c', '--cursor',
                        help='Start from last cursor',
                        dest='useCursor',
                        default=False,
                        required=False,
                        action='store_true')
    parser.add_argument('-l', '--limit',
                        help='Number of records we pull for each chunk when we use --cursor. Default is 100',
                        dest='limit',
                        default=100,
                        required=False)
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
    try:
        logger.debug('begin processing......')
        process(args, auditclient, utils)
    except Exception as e:
        logging.exception(e)


def process(args, auditclient, utils):

    logger.debug('fetching cursor.......')

    cursor = utils.getnextPageCursor()
    nextPageCursor = None if not cursor else cursor['nextPageCursor']
    lastRecordId = None if not cursor else cursor['lastRecordSaved']

    logger.debug('nextPageCursor: %s' % (nextPageCursor))

    queryStart = args.startDate
    queryEnd = args.endDate

    # Check dates are in valid IS08601 format
    iso8601.parse_date(queryStart)
    iso8601.parse_date(queryEnd)

    safeFilename = args.safeFilename
    jsonFolderPath = args.json
    csvFolderPath = args.csv
    syslogHost = args.sysloghost
    syslogPort = args.syslogport
    useCursor = args.useCursor
    limit = args.limit

    logger.debug('useCursor: %s' % (useCursor))

    # Syslog logger
    syslogger = None if syslogHost is None else utils.configSysLogger(
        syslogHost, syslogPort)

    req = {
        'method': 'GET',
        'query': {
            'start': queryStart,
            'end': queryEnd,
            'sort': 'timestamp:asc',
        }
    }

    if(nextPageCursor and useCursor):
        req['query']['cursor'] = nextPageCursor

    req['query']['limit'] = limit

    hasMore = True
    iteration = 1
    writeHeaders = {}

    logger.debug('fetching audit records....')
    while hasMore:
        payload = auditclient.fetchRecords(req)
        records = payload['data'] if not cursor else utils.checkRecords(
            payload['data'], lastRecordId)
        if(len(records)):
            lastRecordId = records[-1]['recordId']
        else:
            hasMore = False
            break

        if(jsonFolderPath and len(records)):
            utils.exportToJson(jsonFolderPath, records, safeFilename)
        if(csvFolderPath and len(records)):
            utils.exportToCsv(csvFolderPath, records, writeHeaders)
        if(syslogHost is not None and len(records)):
            utils.exportToSysLog(syslogHost, syslogPort,
                                 syslogger, records)

        if 'after' in payload['cursor']:
            logger.debug('found next cursor')
            nextPageCursor = payload['cursor']['after']
            req['query']['cursor'] = nextPageCursor
        else:
            hasMore = False

        if(useCursor):
            utils.saveNextPageCursor(nextPageCursor, lastRecordId)

        cursorToPrint = str(nextPageCursor) if hasMore else 'None'

        print('Iteration :' + str(iteration) + '\t\t' + 'Items: ' +
              str(len(records)) + '\t\t' + 'nextPageCursor: ' + cursorToPrint)
        iteration += 1
    
    if not hasMore and iteration == 1:
        print('No records found / exported.')
    else:
        print('All records exported!!!!')
