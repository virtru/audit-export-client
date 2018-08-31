import jwt
import base64
import random
import time
import hashlib
import requests

def generateNonce(length=8):
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


def generateRsha(method, host, path, queryParams):
    hash = hashlib.sha256(method + host + path + queryParams).digest()
    b64Hash = base64.urlsafe_b64encode(hash)

    # Remove padding
    b64Hash = b64Hash.replace('=', '')
    return b64Hash


def getJson(apiTokenId, apiTokenSecret, apiHost, apiPath,apiQueryStart,apiQueryEnd):

    tokenSecret = base64.b64decode(apiTokenSecret)
    method = 'GET'
    queryParams = 'start={0}end={1}'.format(apiQueryStart, apiQueryEnd)
    nonce = generateNonce()

    payload = {
        'sub': apiTokenId,
        'iat': int(time.time()),
        'jti': nonce,
        'rsha': generateRsha(method, apiHost, apiPath, queryParams),
        'rqps': 'start,end',
        'exp': int(time.time()+60.0)
    }

    encoded = jwt.encode(payload, tokenSecret, algorithm='HS256')


    params = {
        'auth-xport': "header",
        'start': str(apiQueryStart),
        'end': str(apiQueryEnd)
    }
    headers = {
        'authorization': 'VJWTv1.0.0 ' + encoded
    }

    apiUrl = apiHost + apiPath

    response = requests.get("https://" + apiUrl, params=params, headers=headers)

    return response.text

def getJsonBookmark(apiTokenId, apiTokenSecret, apiHost, apiPath,apiQueryStart,apiQueryEnd,apiBookmark):

    tokenSecret = base64.b64decode(apiTokenSecret)
    method = 'GET'
    queryParams = 'start={0}end={1}'.format(apiQueryStart, apiQueryEnd)
    nonce = generateNonce()

    payload = {
        'sub': apiTokenId,
        'iat': int(time.time()),
        'jti': nonce,
        'rsha': generateRsha(method, apiHost, apiPath, queryParams),
        'rqps': 'start,end',
        'exp': int(time.time()+60.0)
    }

    encoded = jwt.encode(payload, tokenSecret, algorithm='HS256')


    params = {
        'auth-xport': "header",
        'start': str(apiQueryStart),
        'end': str(apiQueryEnd),
        'nextPageStartKey': str(apiBookmark)
    }
    headers = {
        'authorization': 'VJWTv1.0.0 ' + encoded
    }

    apiUrl = apiHost + apiPath

    response = requests.get("https://" + apiUrl, params=params, headers=headers)

    return response.text
