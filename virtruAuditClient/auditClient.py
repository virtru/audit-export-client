import random
import hashlib
import base64
import requests
import jwt
import time
import sys
import logging
import .utils

VJWT_TTL_SECONDS = 60.0


class AuditClient:
    def __init__(self, apiTokenSecret, apiTokenId, apiHost, apiPath):
        self.apiTokenSecret = apiTokenSecret
        self.apiTokenId = apiTokenId
        self.apiHost = apiHost
        self.apiPath = apiPath

    def process(self, req, jsonFolderPath, csvFolderPath, syslogHost):
        hasMore = True
        iteration = 1

        while hasMore:
            try:
                records = self.__fetchRecords(req)
                if(jsonFolderPath and records['docs']):
                    utils.exportToJson(jsonFolderPath, records['docs'])
                if(csvFolderPath and records['docs']):
                    utils.exportToCsv(csvFolderPath, records['docs'])
                if(syslogHost is not None and syslogPort is not None and records['docs']):
                    utils.exportToSysLog(
                        syslogHost, syslogPort, records['docs'])

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
            except (FileNotFoundError, ConnectionError) as err:
                logging.error(err)
                sys.exit(-1)

    def __fetchRecords(self, req):
        vjwtString = self.__generateVjwtString(req)

        headers = {
            'Authorization': 'VJWTv1.0.0 ' + vjwtString.decode()
        }

        apiUrl = self.apiHost + self.apiPath
        try:
            response = requests.get("https://" + apiUrl,
                                    params=req['query'], headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(
                'An Error occured while trying to fetch records, verify the information in your config.ini')
            sys.exit(1)

        return response.json()

    def __generateVjwtString(self, req):
        tokenSecret = base64.b64decode(self.apiTokenSecret)
        method = req['method']

        queryParams = self.__generateQueryParams(req['query'])
        nonce = self.__generateNonce()

        payload = {
            'sub': self.apiTokenId,
            'iat': int(time.time()),
            'jti': nonce,
            'rsha': self.__generateRsha(method, self.apiHost, self.apiPath, queryParams),
            'rqps': ','.join(req['query'].keys()),
            'exp': int(time.time()+VJWT_TTL_SECONDS)
        }
        return jwt.encode(payload, tokenSecret, algorithm='HS256')

    def __generateQueryParams(self, query):
        result = ''
        for key, value in query.items():
            result = result+"%s=%s" % (key, value)
        return result

    def __generateNonce(self, length=8):
        return ''.join([str(random.randint(0, 9)) for i in range(length)])

    def __generateRsha(self, method, host, path, queryParams):
        hash = hashlib.sha256(
            (method + host + path + queryParams).encode('utf-8')).digest()
        b64Hash = base64.urlsafe_b64encode(hash)

        # Remove padding
        b64Hash = b64Hash.decode().replace('=', '')
        return b64Hash
