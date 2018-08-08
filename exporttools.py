import json
import apitoken
import appidbundle
import contractget
import dlprules
import encryptedsearch
import licenseinvitation
import organization
import policy
import unitattributes
import usersettings
import syslogclient
import platform
import os

def tojson(folder, filename, jsonin):
    filename = filename.replace(':','-')
    fn = os.path.join(folder, filename)
    with open(fn, "w") as f:
        json.dump(jsonin, f, sort_keys=True, indent=4, separators=(',', ': '))


def tocsv(csvfolder,
          listApiToken,
          listAppIdBundle,
          listContractGet,
          listDlpRules,
          listEncryptedSearch,
          listLicenseInvitation,
          listOrganization,
          listPolicy,
          listUnitAttributes,
          listUserSettings):
    with open(os.path.join(csvfolder,'apitoken.csv'), "a") as csvApiToken:
        for curr in listApiToken:
            csvApiToken.write(curr.tocsv())
            csvApiToken.write("\n")
    with open(os.path.join(csvfolder,'appidbundle.csv'), "a") as csvAppIdBundle:
        for curr in listAppIdBundle:
            csvAppIdBundle.write(curr.tocsv())
            csvAppIdBundle.write("\n")
    with open(os.path.join(csvfolder,'contractget.csv'), "a") as csvContractGet:
        for curr in listContractGet:
            csvContractGet.write(curr.tocsv())
            csvContractGet.write("\n")
    with open(os.path.join(csvfolder,'dlprules.csv'), "a") as csvDlpRules:
        for curr in listDlpRules:
            csvDlpRules.write(curr.tocsv())
            csvDlpRules.write("\n")
    with open(os.path.join(csvfolder,'encryptedsearchkey.csv'), "a") as csvEncryptedSearch:
        for curr in listEncryptedSearch:
            csvEncryptedSearch.write(curr.tocsv())
            csvEncryptedSearch.write("\n")
    with open(os.path.join(csvfolder,'licenseinvitation.csv'), "a") as csvLicenseInvitation:
        for curr in listLicenseInvitation:
            csvLicenseInvitation.write(curr.tocsv())
            csvLicenseInvitation.write("\n")
    with open(os.path.join(csvfolder,'organization.csv'), "a") as csvOrganization:
        for curr in listOrganization:
            csvOrganization.write(curr.tocsv())
            csvOrganization.write("\n")
    with open(os.path.join(csvfolder,'policy.csv'), "a") as csvPolicy:
        for curr in listPolicy:
            csvPolicy.write(curr.tocsv())
            csvPolicy.write("\n")
    with open(os.path.join(csvfolder,'unitattributes.csv'), "a") as csvUnitAttributes:
        for curr in listUnitAttributes:
            csvUnitAttributes.write(curr.tocsv())
            csvUnitAttributes.write("\n")
    with open(os.path.join(csvfolder,'usersettings.csv'), "a") as csvUserSettings:
        for curr in listUserSettings:
            csvUserSettings.write(curr.tocsv())
            csvUserSettings.write("\n")


def tosyslog(sysloghost, syslogport,
             listApiToken,
             listAppIdBundle,
             listContractGet,
             listDlpRules,
             listEncryptedSearch,
             listLicenseInvitation,
             listOrganization,
             listPolicy,
             listUnitAttributes,
             listUserSettings):
    prefix1 = '<22>1'
    hostName = platform.node()
    prefix2 = 'VirtruAuditAPI 10 0 audit@200'
    prefix = prefix1 + ' ' + str(hostName) + ' ' + prefix2
    syslogSend = syslogclient.Syslog(host=sysloghost, port=int(syslogport))
    for curr in listApiToken:
        syslogSend.send(prefix, curr.tosyslog(), syslogclient.Level.INFO)
    for curr in listAppIdBundle:
        syslogSend.send(prefix, curr.tosyslog(), syslogclient.Level.INFO)
    for curr in listContractGet:
        syslogSend.send(prefix, curr.tosyslog(), syslogclient.Level.INFO)
    for curr in listDlpRules:
        syslogSend.send(prefix, curr.tosyslog(), syslogclient.Level.INFO)
    for curr in listEncryptedSearch:
        syslogSend.send(prefix, curr.tosyslog(), syslogclient.Level.INFO)
    for curr in listLicenseInvitation:
        syslogSend.send(prefix, curr.tosyslog(), syslogclient.Level.INFO)
    for curr in listOrganization:
        syslogSend.send(prefix, curr.tosyslog(), syslogclient.Level.INFO)
    for curr in listPolicy:
        syslogSend.send(prefix, curr.tosyslog(), syslogclient.Level.INFO)
    for curr in listUnitAttributes:
        syslogSend.send(prefix, curr.tosyslog(), syslogclient.Level.INFO)
    for curr in listUserSettings:
        syslogSend.send(prefix, curr.tosyslog(), syslogclient.Level.INFO)


def jsontolist(jsonin):
    listAuditData = []
    itemcount = len(jsonin['docs'])
    for x in range(itemcount):
        if (jsonin['docs'][x]['type']) == 'encrypted-search-key':
            co = encryptedsearch.EncryptedSearch()
            co.loadjson(jsonin['docs'][x])
        elif (jsonin['docs'][x]['type']) == 'contract-get':
            co = contractget.ContractGet()
            co.loadjson(jsonin['docs'][x])
        elif (jsonin['docs'][x]['type']) == 'api-token':
            co = apitoken.ApiToken()
            co.loadjson(jsonin['docs'][x])
        elif (jsonin['docs'][x]['type']) == 'policy':
            co = policy.Policy()
            co.loadjson(jsonin['docs'][x])
        elif (jsonin['docs'][x]['type']) == 'appIdBundle':
            co = appidbundle.AppIdBundle()
            co.loadjson(jsonin['docs'][x])
        elif (jsonin['docs'][x]['type']) == 'organization':
            co = organization.Organization()
            co.loadjson(jsonin['docs'][x])
        elif (jsonin['docs'][x]['type']) == 'dlp-rules':
            co = dlprules.DlpRules()
            co.loadjson(jsonin['docs'][x])
        elif (jsonin['docs'][x]['type']) == 'unit-attributes':
            co = unitattributes.UnitAttributes()
            co.loadjson(jsonin['docs'][x])
        elif (jsonin['docs'][x]['type']) == 'userSettings':
            co = usersettings.UserSettings()
            co.loadjson(jsonin['docs'][x])
        elif (jsonin['docs'][x]['type']) == 'licenseInvitation':
            co = licenseinvitation.LicenseInvitation()
            co.loadjson(jsonin['docs'][x])
        else:
            print(jsonin['docs'][x]['type'])

        listAuditData.append(co)
    return listAuditData


def exportjson(listAuditData, iscsv, csvfolder, issyslog, sysloghost, syslogport):
    listApiToken = []
    listAppIdBundle = []
    listContractGet = []
    listDlpRules = []
    listEncryptedSearch = []
    listLicenseInvitation = []
    listOrganization = []
    listPolicy = []
    listUnitAttributes = []
    listUserSettings = []

    for curr in listAuditData:
        if curr.type == 'api-token':
            listApiToken.append(curr)
        elif curr.type == 'appIdBundle':
            listAppIdBundle.append(curr)
        elif curr.type == 'contract-get':
            listContractGet.append(curr)
        elif curr.type == 'dlp-rules':
            listDlpRules.append(curr)
        elif curr.type == 'encrypted-search-key':
            listEncryptedSearch.append(curr)
        elif curr.type == 'licenseInvitation':
            listLicenseInvitation.append(curr)
        elif curr.type == 'organization':
            listOrganization.append(curr)
        elif curr.type == 'policy':
            listPolicy.append(curr)
        elif curr.type == 'unit-attributes':
            listUnitAttributes.append(curr)
        elif curr.type == 'userSettings':
            listUserSettings.append(curr)

    if iscsv:
        tocsv(csvfolder,
              listApiToken,
              listAppIdBundle,
              listContractGet,
              listDlpRules,
              listEncryptedSearch,
              listLicenseInvitation,
              listOrganization,
              listPolicy,
              listUnitAttributes,
              listUserSettings)

    if issyslog:
        tosyslog(sysloghost, syslogport,
                 listApiToken,
                 listAppIdBundle,
                 listContractGet,
                 listDlpRules,
                 listEncryptedSearch,
                 listLicenseInvitation,
                 listOrganization,
                 listPolicy,
                 listUnitAttributes,
                 listUserSettings)
