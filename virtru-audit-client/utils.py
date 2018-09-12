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

BOOK_MARK_FILE_NAME = 'bookmark.ini'


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


class AuditTypes(Enum):
    API_TOKEN = 'api-token'
    APP_ID_BUNDLE = 'appIdBundle'
    CONTRACT_GET = 'contract-get'
    DLP_RULES = 'dlp-rules',
    DLP_OVERRIDE = 'dlpOverride'
    ENCRYPTED_SEARCH_KEY = 'encrypted-search-key'
    LICENSE_INVITATION = 'licenseInvitation'
    ORGANIZATION = 'organization'
    POLICY = 'policy'
    UNIT_ATTRIBUTES = 'unit-attributes'
    USER_SETTINGS = 'userSettings'


def getConfig(configFile):
    try:
        config = configparser.ConfigParser()
        with open(configFile) as f:
            config.read_file(f)
        return config['ApiInfo']
    except FileNotFoundError as err:
        logging.error(err)
        sys.exit(-1)


def getNextPageStartKey():
    bookmark = configparser.ConfigParser()
    bookmark.read(BOOK_MARK_FILE_NAME)
    if len(bookmark) <= 1:
        return None
    else:
        return bookmark['next-page-start-key']


def saveNextPageStartKey(nextPageStartKey):
    bookMarkConfig = configparser.ConfigParser()
    bookMarkConfig['next-page-start-key'] = {
        'nextPageStartKey': nextPageStartKey}
    with open(BOOK_MARK_FILE_NAME, 'w') as bookMarkFile:
        bookMarkConfig.write(bookMarkFile)


def exportToJson(pathToFolder, records):

    fileName = str(datetime.datetime.utcnow().isoformat()) + ".json"
    fn = os.path.join(pathToFolder, fileName)
    with open(fn, "w") as f:
        json.dump(records, f, sort_keys=True,
                  indent=4, separators=(',', ': '))


def exportToCsv(pathToFolder, records):
    for record in records:
        auditType = record['type']
        fileName = auditType + ".csv"
        __writeCsvFile(auditType, pathToFolder, fileName, record)


def exportToSysLog(host, port, records):
    logger = logging.getLogger('virtru-export')
    logger.setLevel(logging.INFO)

    format = '%(isotime)s %(hostname)s %(name)s %(process)d - [data@22 %(data)s] %(message)s'
    formatter = RFC5424Formatter(format)
    sh = logging.handlers.SysLogHandler(
        address=(host, int(port)), facility=SysLogHandler.LOG_DAEMON)
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    for record in records:
        formattedRecord = {k: ('\"-\"' if v == [] or v == '' else ','.join(v) if isinstance(v, list) else v)
                           for (k, v) in record.items()}
        formattedStructData = " ".join(
            ["=".join([key, str(val)]) for key, val in formattedRecord.items()])

        adapter = logging.LoggerAdapter(
            logger, {'data': str(formattedStructData)})
        adapter.info('virtru-audit-%s', record['type'])


def __writeCsvFile(auditType, pathToFolder, fileName, record):
    filePath = os.path.join(pathToFolder, fileName)
    with open(filePath, 'a', newline='') as csvfile:
        fieldnames = record.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(record)
