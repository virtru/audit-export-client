import config
import restclient
import exporttools
import json
import argparse
import datetime


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
                        required=False)
    parser.add_argument('-e', '--end',
                        help='End date of query.  Example: -e 2019-02-01',
                        dest='endDate',
                        required=False)
    parser.add_argument('--csv',
                        help='CSV output folder.  If defined CSV will be exported',
                        dest='csv',
                        required=False)
    parser.add_argument('--json',
                        help='Json output folder.  If defined Json will be exported.  Example: output/  '
                             '/home/user/json/',
                        dest='json',
                        required=False)
    parser.add_argument('--syslog',
                        help='Syslog server.  If defined syslog will be exported',
                        dest='syslog',
                        required=False)
    parser.add_argument('--syslogport',
                        help='Syslog port.  If a different port is required.',
                        dest='syslogport',
                        default='514',
                        required=False)
    parser.add_argument('-b', '--usebookmark',
                        help='Use bookmark to track runs.  New run will only pull new data.',
                        dest='isbookmark',
                        action='store_true',
                        default=False,
                        required=False)

    args = parser.parse_args()

    if args.startDate is None:
        querystart = '2010-01-01'
    else:
        querystart = args.startDate

    if args.endDate is None:
        queryend = '2100-01-01'
    else:
        queryend = args.endDate

    if args.csv is None:
        iscsv = False
        outputcsv = u''
    else:
        iscsv = True
        outputcsv = args.csv

    if args.json is None:
        isjson = False
        outputjson = u''
    else:
        isjson = True
        outputjson = args.json

    if args.syslog is None:
        issyslog = False
        sysloghost = u'localhost'
    else:
        issyslog = True
        sysloghost = args.syslog

    isbookmark = args.isbookmark
    syslogport = args.syslogport

    configfile = args.configFile

    c = config.Config(configfile)

    iteration = 1
    hasMore = True
    isFirstRun = True
    apiBookmark = ''
    if isbookmark:
        hasBookmark = c.bookmarkexists()
        if hasBookmark:
            apiBookmark = c.getbookmark()

    while hasMore:
        try:
            if isFirstRun and isbookmark:
                if hasBookmark:
                    response = restclient.getJsonBookmark(c.apiTokenId, c.apiTokenSecret, c.apiHost, c.apiPath,
                                                          querystart, queryend, apiBookmark)
                else:
                    response = restclient.getJson(c.apiTokenId, c.apiTokenSecret, c.apiHost, c.apiPath,
                                                          querystart, queryend)
                isFirstRun = False
            elif isFirstRun:
                response = restclient.getJson(c.apiTokenId, c.apiTokenSecret, c.apiHost, c.apiPath,
                                                      querystart, queryend)
                isFirstRun = False
            else:
                apiBookmark = str(responsejson['nextPageStartKey'])
                response = restclient.getJsonBookmark(c.apiTokenId, c.apiTokenSecret, c.apiHost, c.apiPath, querystart,
                                                      queryend, apiBookmark)
            responsejson = json.loads(response)

            print('Iteration :' + str(iteration) + '\t\t' + "Items: " + str(len(responsejson['docs'])) + '\t' +
                  'Bookmark: ' + apiBookmark)
            iteration += 1
            if len(responsejson.keys()) == 3:
                hasMore = True
            else:
                hasMore = False
                if isbookmark:
                    if len(responsejson['docs']) > 0:
                        c.setbookmark(str(responsejson['docs'][(len(responsejson['docs'])-1)]['recordId']))

            list_audit_data = exporttools.jsontolist(responsejson)
            exporttools.exportjson(list_audit_data, iscsv, outputcsv, issyslog, sysloghost, syslogport)
            if isjson:
                a = str(datetime.datetime.utcnow().isoformat()) + ".json"
                exporttools.tojson(outputjson, a, responsejson)
        except IOError as err:
            print("Error has occurred while trying to poll for data")
            print(u'{0}'.format(err))
       

if __name__ == "__main__":
    main()
