import configparser
import datetime
import time
import os
import json
import sys
import csv
import pathlib
import logging
import socket
import re
from enum import Enum
from logging.handlers import SysLogHandler
from .auditclient.errors import AuditClientError

BOOK_MARK_FILE_NAME = 'bookmark.ini'

logger = logging.getLogger(__name__)


class RFC5424Formatter(logging.Formatter):
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


def getNextPageStartKey():
    bookmark = configparser.ConfigParser()
    bookmark.read(BOOK_MARK_FILE_NAME)

    # Config Parser returns an empty dataset if file does not exist
    if len(bookmark) <= 1:
        return None
    else:
        return bookmark['next-page-start-key']


def saveNextPageStartKey(nextPageStartKey):
    logger.debug('saving nexpagestartkey.....')

    bookMarkConfig = configparser.ConfigParser()
    bookMarkConfig['next-page-start-key'] = {
        'nextPageStartKey': nextPageStartKey}
    with open(BOOK_MARK_FILE_NAME, 'w') as bookMarkFile:
        bookMarkConfig.write(bookMarkFile)


def exportToJson(pathToFolder, records):
    logger.debug('exporting records to json.....')

    fileName = str(datetime.datetime.utcnow().isoformat()) + ".json"
    fn = os.path.join(pathToFolder, fileName)
    with open(fn, "w") as f:
        json.dump(records, f, sort_keys=True,
                  indent=4, separators=(',', ': '))


def exportToCsv(pathToFolder, records):
    logger.debug('exporting records to csv.....')

    for record in records:
        auditType = record['type']
        fileName = auditType + ".csv"
        __writeCsvFile(auditType, pathToFolder, fileName, record)


def exportToSysLog(host, port, syslogger, records):
    logger.debug('exporting to records to syslog......')

    format = '%(isotime)s %(hostname)s %(name)s %(process)d - [data@22 %(data)s] %(message)s'
    formatter = RFC5424Formatter(format)

    # sysloghandler = logging.handlers.SysLogHandler(
    #     address='/var/run/syslog', facility=SysLogHandler.LOG_INFO)
    sysloghandler = logging.handlers.SysLogHandler(
        address=(host, int(port)), facility=SysLogHandler.LOG_DAEMON)

    sysloghandler.setLevel(logging.INFO)
    sysloghandler.setFormatter(formatter)
    syslogger.addHandler(sysloghandler)

    # streamhandler = logging.StreamHandler()
    # streamhandler.setLevel(logging.INFO)
    # streamhandler.setFormatter(formatter)
    # logger.addHandler(streamhandler)

    for record in records:
        # Flatten out dictionary
        formattedRecord = __flatten(record)

        # Construct structured data
        formattedStructData = " ".join(
            ["=".join([key, "\"{}\"".format(str(val))]) for key, val in formattedRecord.items()])

        adapter = logging.LoggerAdapter(
            syslogger, {'data': str(formattedStructData)})
        adapter.info('virtru-audit-%s', record['type'])

        # adapter2 = logging.LoggerAdapter(
        #     logger, {'data': str(formattedStructData)})
        # adapter2.info('virtru-audit-%s', record['type'])

    logger.debug('closing syslogport......')
    sysloghandler.close()


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


def __writeCsvFile(auditType, pathToFolder, fileName, record):
    filePath = os.path.join(pathToFolder, fileName)
    with open(filePath, 'a', newline='') as csvfile:
        fieldnames = record.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(record)


class InvalidConfigError(AuditClientError):
    def __init__(self):
        msg = 'An error occured while reading config file'
        super().__init__(msg)
