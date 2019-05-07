
import random
import hashlib
import base64
import binascii
import requests
import jwt
import time
import sys
import logging
from binascii import Error
from . import errors

logger = logging.getLogger(__name__)

VJWT_TTL_SECONDS = 300.0
API_HOST = 'audit.virtru.com'
API_PATH = '/api/messages'
CLIENT_NAME = 'AuditPythonClient:v2.0.0'
API_VERSION = 'v2'
IAT_LEEWAY_SECONDS = 300.0


class AuditClient:
    """Audit Client for fetching audit records."""

    def __init__(self, apiTokenSecret, apiTokenId, apiHost=API_HOST, apiPath=API_PATH):
        """ AuditClient class constructor

        Arguments:
            apiTokenSecret {String} -- The apiTokenSecret provided by Virtru.
            apiTokenId {String} -- The apiTokenId proviced by Virtru.
            apiHost {[String]} -- The apiHost. Defaults to audit.virtru.com.
            apiPath {[String]} -- The apiPath. Defaults to /api/messages.
        """

        self.apiTokenSecret = apiTokenSecret
        self.apiTokenId = apiTokenId
        self.apiHost = apiHost
        self.apiPath = apiPath

    def fetchRecords(self, req):
        """ Fetch audit records

        Arguments:
            req {Dictionary} -- request Dictionary
                e.g. {
                    method: GET,
                    query: {
                        start: 2000,
                        end: 2018
                    }
                }


        Returns:
            Dictionary -- repsponse object

            The response dictionary has the following format:
                {
                    docs: [{Dictonary}],
                    nextPageStartKey: {String}
                }
        """

        vjwtString = self._generateVjwtString(req)

        headers = {
            'Authorization': 'VJWTv1.0.0 ' + vjwtString.decode(),
            'Connection': 'close',
            'X-Virtru-Client': CLIENT_NAME,
            'Accept-Version': API_VERSION
        }
        apiUrl = self.apiHost + self.apiPath

        response = requests.get("https://" + apiUrl,
                                params=req['query'], headers=headers)

        self._validateResponse(response.status_code)

        return response.json()

    def _validateResponse(self, statusCode):
        """Validates response """
        def status401():
            raise errors.InvalidCredentialsError()

        def default():
            raise errors.ClientConnectionError(statusCode)

        def status200():
            pass

        def switch(arg):
            switcher = {
                401: status401,
                403: status401,
                200: status200
            }
            switcher.get(arg, default)()

        switch(statusCode)

    def _generateVjwtString(self, req):
        """Generate vjwt authorization string to be included in authorization of requests

        Arguments:
            req {Dictonary} -- request dictionary.

        Returns:
            String -- The authorization string.
        """
        try:
            tokenSecret = base64.b64decode(self.apiTokenSecret)
        except (TypeError, binascii.Error) as err:
            raise errors.InvalidCredentialsError(
                'The provided ApiSecret/ApiId are invalid')

        method = req['method']
        queryKeys = req['query'].keys()

        queryParams = self._generateQueryParams(req['query'], queryKeys)
        nonce = self._generateNonce()

        payload = {
            'sub': self.apiTokenId,
            'iat': int(time.time()-IAT_LEEWAY_SECONDS),
            'jti': nonce,
            'rsha': self._generateRsha(method, self.apiHost, self.apiPath, queryParams),
            'rqps': ','.join(queryKeys),
            'exp': int(time.time()+VJWT_TTL_SECONDS)
        }
        return jwt.encode(payload, tokenSecret, algorithm='HS256')

    def _generateQueryParams(self, query, keys):
        """Generate string of query

        Arguments:
            query {OrderedDict} -- dictionary containing query params.
                e.g. {
                    start: 2000,
                    end: 2019
                }
            key {List} -- List of keys

        Returns:
            String -- query string. e.g. start=2000end==2019
        """

        result = ''
        for key in keys:
            result = result+'%s=%s' % (key, query[key])
        return result

    def _generateNonce(self, length=8):
        """Generate nonce"""
        return ''.join([str(random.randint(0, 9)) for i in range(length)])

    def _generateRsha(self, method, host, path, queryParams):
        """Generate Base64UrlEncode of SHA256 hash of the Method + host + path + query params + headers"""
        hash = hashlib.sha256(
            (method + host + path + queryParams).encode('utf-8')).digest()
        b64Hash = base64.urlsafe_b64encode(hash)

        # Remove padding
        b64Hash = b64Hash.decode().replace('=', '')
        return b64Hash
