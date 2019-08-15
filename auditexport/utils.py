import configparser, datetime, time, os, json, sys, csv, pathlib, logging, socket, re
from logging.handlers import SysLogHandler
from .auditclient.errors import AuditClientError

EXPORT_DIR = '.auditexport'
CURSOR_PATH = '%s/cursor.ini' % (EXPORT_DIR)


logger = logging.getLogger(__name__)


class RFC5424Formatter(logging.Formatter):

    # RFC5424 formater by author:specialunderwear
    # https://github.com/specialunderwear/python-rfc5424-logging-formatter

    def __init__(self, *args, **kwargs):

        self._tz_fix = re.compile(r'([+-]\d{2})(\d{2})$')
        super(RFC5424Formatter, self).__init__(*args, **kwargs)

    def format(self, record):
        try:
            record.__dict__['hostname'] = socket.gethostname()
        except:
            record.__dict__['hostname'] = '-'
        isotime = datetime.datetime.fromtimestamp(record.created).isoformat()
        tz = self._tz_fix.match(time.strftime('%z'))
        if time.timezone and tz:
            (offset_hrs, offset_min) = tz.groups()
            isotime = '{0}{1}:{2}'.format(isotime, offset_hrs, offset_min)
        else:
            isotime = isotime + 'Z'

        record.__dict__['isotime'] = isotime

        return super(RFC5424Formatter, self).format(record)


def getConfig(configFile=''):
    config = configparser.ConfigParser()
    apiTokenSecret = ''
    apiTokenId = ''
    apiHost = ''
    apiPath = ''

    with open(configFile) as f:
        config.read_file(f)

    try:
        apiTokenSecret = config['ApiInfo']['apiTokenSecret']
        apiTokenId = config['ApiInfo']['apiTokenId']
        apiHost = config['ApiInfo']['apiHost']
        apiPath = config['ApiInfo']['apiPath']
    except KeyError as e:
        raise InvalidConfigError

    return {
        'apiTokenSecret': apiTokenSecret,
        'apiTokenId': apiTokenId,
        'apiHost': apiHost,
        'apiPath': apiPath
    }

def checkRecords(records=[], savedId=None):
    if not savedId:
        return records
    for i in range(len(records)):
        if records[i]['recordId'] == savedId:
            return records[i+1:]
    return records


def getnextPageCursor():
    cursor = configparser.ConfigParser()
    cursor.read(CURSOR_PATH)

    # Config Parser returns an empty dataset if file does not exist
    if len(cursor) <= 1:
        return None
    else:
        return cursor['next-page-cursor']

def flattenObjectProp(record):
    editedRecord = {**record, **record['object']}
    del(editedRecord['object'])
    return editedRecord

def saveNextPageCursor(nextPageCursor, lastRecordSaved):
    logger.debug('saving next-page-cursor.....')

    cursorConfig = configparser.ConfigParser()
    cursorConfig['next-page-cursor'] = {
        'nextPageCursor': nextPageCursor or '',
        'lastRecordSaved': lastRecordSaved
    }
    os.makedirs(os.path.dirname(CURSOR_PATH), exist_ok=True)
    with open(CURSOR_PATH, 'w') as cursorFile:
        cursorConfig.write(cursorFile)

def pre_export(fileFormat, records):
    logger.debug('exporting records to ' + fileFormat + '.....')
    preparedRecords = [flattenObjectProp(record) for record in records]
    return preparedRecords


def exportToJson(pathToFolder, records):
    preparedRecords = pre_export('json', records)

    fileName = str(datetime.datetime.utcnow().isoformat()) + '.json'
    fn = os.path.join(pathToFolder, fileName)
    with open(fn, 'w') as f:
        json.dump(preparedRecords, f, sort_keys=True,
                  indent=4, separators=(',', ': '))


def exportToCsv(pathToFolder, records, writeHeaders):
    preparedRecords = pre_export('csv', records)

    for record in preparedRecords:
        auditType = record['type']
        fileName = auditType + '.csv'
        filePath = os.path.join(pathToFolder, fileName)

        # Write header only once for each auditType
        writeHeader = (
            writeHeaders[record['type']]) = (
                record['type'] not in writeHeaders)

        __writeCsvFile(auditType, filePath, record, writeHeader)


def exportToSysLog(host, port, syslogger, records):
    preparedRecords = pre_export('syslog', records)

    for record in preparedRecords:
        # Flatten out dictionary
        formattedRecord = __flatten(record)

        # Construct structured data
        formattedStructData = ' '.join(
            ['='.join([key, '"{}"'.format(str(val))]) for key, val in formattedRecord.items()])

        adapter = logging.LoggerAdapter(
            syslogger, {'data': str(formattedStructData)})
        adapter.info('virtru-audit-%s', record['type'])


def configSysLogger(host, port):
    syslogger = logging.getLogger('virtru-export')
    syslogger.setLevel(logging.INFO)
    format = '%(isotime)s %(hostname)s %(name)s %(process)d - [data@22 %(data)s] %(message)s'
    formatter = RFC5424Formatter(format)
    sysloghandler = logging.handlers.SysLogHandler(
        address=(host, int(port)), facility=SysLogHandler.LOG_DAEMON)
    sysloghandler.setLevel(logging.INFO)
    sysloghandler.setFormatter(formatter)
    syslogger.addHandler(sysloghandler)
    return syslogger


def __flatten(dic):
    for k, v in dic.items():
        if isinstance(v, list):
            items = []
            for x in v:
                if isinstance(x, dict):
                    for (k1, v2) in x.items():
                        items.append('{}={}'.format(k1, str(v2)))
                else:
                    items.append(str(x))
            if items:
                dic[k] = ','.join(items)
        if v == [] or v == '':
            dic[k] = '-'

    return dic


def __writeCsvFile(auditType, filePath, record, writeHeader):
    operation = 'w' if writeHeader else 'a'

    with open(filePath, operation, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=record.keys())
        writer.writeheader() if writeHeader else writer.writerow(record)


class InvalidConfigError(AuditClientError):
    def __init__(self):
        msg = 'An error occured while reading config file'
        super().__init__(msg)
