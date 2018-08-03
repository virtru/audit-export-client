class DlpRules:

    def __init__(self):
        self.isDeprecated = False
        self.requestIp = ''
        self.virtruClient = ''
        self.displayName = ''
        self.created = ''
        self.recordId = ''
        self.timestamp = ''
        self.ruleId = ''
        self.userId = ''
        self.orgId = ''
        self.ous = []
        self.dlpActions = []
        self.orgActionType = ''
        self.requestId = ''
        self.groups = []
        self.lastModified = ''
        self.action = ''
        self.userAgent = ''
        self.type = ''
        self.scope = ''

    def loadjson(self, jsonin):
        self.isDeprecated = jsonin.get('isDeprecated', False)
        self.requestIp = jsonin.get('requestIp', '')
        self.virtruClient = jsonin.get('virtruClient', '')
        self.displayName = jsonin.get('displayName', '')
        self.created = jsonin.get('created', '')
        self.recordId = jsonin.get('recordId', '')
        self.timestamp = jsonin.get('timestamp', '')
        self.ruleId = jsonin.get('ruleId', '')
        self.userId = jsonin.get('userId', '')
        self.orgId = jsonin.get('orgId', '')
        self.ous = jsonin.get('ous', None)
        self.dlpActions = jsonin.get('dlpActions', None)
        self.orgActionType = jsonin.get('orgActionType', '')
        self.requestId = jsonin.get('requestId', '')
        self.groups = jsonin.get('groups', None)
        self.lastModified = jsonin.get('lastModified', '')
        self.action = jsonin.get('action', '')
        self.userAgent = jsonin.get('userAgent', '')
        self.type = jsonin.get('type', '')
        self.scope = jsonin.get('scope', '')

    def __str__(self):
        r0 = ','
        r1 = '"{0}"'.format(self.timestamp.encode('utf8'))
        r2 = '"{0}"'.format(self.type.encode('utf8'))
        r3 = '"{0}"'.format(self.orgId.encode('utf8'))
        r4 = '"{0}"'.format(self.recordId.encode('utf8'))
        
        return r1 + r0 + r2 + r0 + r3 + r0 + r4

    def tocsv(self):
        r0 = ','
        r1 = '"{0}"'.format(self.isDeprecated)
        r2 = '"{0}"'.format(self.requestIp.encode('utf8'))
        r3 = '"{0}"'.format(self.virtruClient.encode('utf8'))
        r4 = '"{0}"'.format(self.displayName.encode('utf8'))
        r5 = '"{0}"'.format(self.created.encode('utf8'))
        r6 = '"{0}"'.format(self.recordId.encode('utf8'))
        r7 = '"{0}"'.format(self.timestamp.encode('utf8'))
        r8 = '"{0}"'.format(self.ruleId.encode('utf8'))
        r9 = '"{0}"'.format(self.userId.encode('utf8'))
        r10 = '"{0}"'.format(self.orgId.encode('utf8'))
        r11 = '"{0}"'.format(self.flatten(self.ous))
        r12 = '"{0}"'.format(self.flatten(self.dlpActions))
        r13 = '"{0}"'.format(self.orgActionType.encode('utf8'))
        r14 = '"{0}"'.format(self.requestId.encode('utf8'))
        r15 = '"{0}"'.format(self.flatten(self.groups))
        r16 = '"{0}"'.format(self.lastModified.encode('utf8'))
        r17 = '"{0}"'.format(self.action.encode('utf8'))
        r18 = '"{0}"'.format(self.userAgent.encode('utf8'))
        r19 = '"{0}"'.format(self.type.encode('utf8'))
        r20 = '"{0}"'.format(self.scope.encode('utf8'))

        ra = r1 + r0 + r2 + r0 + r3 + r0 + r4 + r0 + r5 + r0 + r6 + r0 + r7 + r0 + r8 + r0 + r9 + r0 + r10 + r0
        rb = r11 + r0 + r12 + r0 + r13 + r0 + r14 + r0 + r15 + r0 + r16 + r0 + r17 + r0 + r18 + r0 + r19 + r0 + r20

        return ra + rb

    def tosyslog(self):
        r0 = ' '
        r1 = '"isDeprecated={}"'.format(self.isDeprecated)
        r2 = '"requestIp={}"'.format(self.requestIp.encode('utf8'))
        r3 = '"virtruClient={}"'.format(self.virtruClient.encode('utf8'))
        r4 = '"displayName={}"'.format(self.displayName.encode('utf8'))
        r5 = '"created={}"'.format(self.created.encode('utf8'))
        r6 = '"recordId={}"'.format(self.recordId.encode('utf8'))
        r7 = '"timestamp={}"'.format(self.timestamp.encode('utf8'))
        r8 = '"ruleId={}"'.format(self.ruleId.encode('utf8'))
        r9 = '"userId={}"'.format(self.userId.encode('utf8'))
        r10 = '"orgId={}"'.format(self.orgId.encode('utf8'))
        r11 = '"ous={}"'.format(self.flatten(self.ous))
        r12 = '"dlpActions={}"'.format(self.flatten(self.dlpActions))
        r13 = '"orgActionType={}"'.format(self.orgActionType.encode('utf8'))
        r14 = '"requestId={}"'.format(self.requestId.encode('utf8'))
        r15 = '"groups={}"'.format(self.flatten(self.groups))
        r16 = '"lastModified={}"'.format(self.lastModified.encode('utf8'))
        r17 = '"action={}"'.format(self.action.encode('utf8'))
        r18 = '"userAgent={}"'.format(self.userAgent.encode('utf8'))
        r19 = '"type={}"'.format(self.type.encode('utf8'))
        r20 = '"scope={}"'.format(self.scope.encode('utf8'))

        ra = r1 + r0 + r2 + r0 + r3 + r0 + r4 + r0 + r5 + r0 + r6 + r0 + r7 + r0 + r8 + r0 + r9 + r0 + r10 + r0
        rb = r11 + r0 + r12 + r0 + r13 + r0 + r14 + r0 + r15 + r0 + r16 + r0 + r17 + r0 + r18 + r0 + r19 + r0 + r20

        return ra + rb

    def flatten(self, listin):
        retval = None
        itemcount = 0
        if not (listin is None):
            retval = '('
            for item in listin:
                itemcount += 1
                retval += item.encode('utf8')
                if itemcount < len(listin):
                    retval += ','
            retval += ')'
        return retval

