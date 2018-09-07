import configparser
import datetime
import os
import json
import sys
import csv
import pathlib
import logging
from enum import Enum
from logging.handlers import SysLogHandler
from rfc5424logging import Rfc5424SysLogHandler

BOOK_MARK_FILE_NAME = 'bookmark.ini'


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


def saveNextPgeStartKey(nextPageStartKey):
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
    formatter = logging.Formatter('%(name)s: [%(levelname)s] %(message)s')
    syslogHandler = SysLogHandler(
        address=(host, int(port)), facility=SysLogHandler.LOG_DAEMON)
    sh = Rfc5424SysLogHandler(address='/var/run/syslog')
    syslogHandler.setFormatter(formatter)
    logger.addHandler(syslogHandler)
    logger.addHandler(sh)
    logger.warn('just warning..........')

    for record in records:
        logger.info('%s', record)


def __writeCsvFile(auditType, pathToFolder, fileName, record):
    # validate type is part of defined types
    filePath = os.path.join(pathToFolder, fileName)
    #mode = 'a' if os.path.exists(filePath) else 'w'
    with open(filePath, 'a', newline='') as csvfile:
        fieldnames = record.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(record)
