class ContractGet:

    def __init__(self):
        self.userId = ''
        self.policyId = ''
        self.requestIp = ''
        self.virtruClient = ''
        self.created = ''
        self.recordId = ''
        self.timestamp = ''
        self.orgId = ''
        self.requestId = ''
        self.orgActionType = ''
        self.lastModified = ''
        self.action = ''
        self.userAgent = ''
        self.type = ''
        self.isNoAuth = None

    def loadjson(self, jsonin):
        self.userId = jsonin.get('userId', '')
        self.policyId = jsonin.get('policyId', '')
        self.requestIp = jsonin.get('requestIp', '')
        self.virtruClient = jsonin.get('virtruClient', '')
        self.created = jsonin.get('created', '')
        self.recordId = jsonin.get('recordId', '')
        self.timestamp = jsonin.get('timestamp', '')
        self.orgId = jsonin.get('orgId', '')
        self.requestId = jsonin.get('requestId', '')
        self.orgActionType = jsonin.get('orgActionType', '')
        self.lastModified = jsonin.get('lastModified', '')
        self.action = jsonin.get('action', '')
        self.userAgent = jsonin.get('userAgent', '')
        self.type = jsonin.get('type', '')
        self.isNoAuth = jsonin.get('isNoAuth', None)

    def __str__(self):
        r0 = ','
        r1 = '"{0}"'.format(self.timestamp.encode('utf8'))
        r2 = '"{0}"'.format(self.type.encode('utf8'))
        r3 = '"{0}"'.format(self.orgId.encode('utf8'))
        r4 = '"{0}"'.format(self.recordId.encode('utf8'))
                            
        return r1 + r0 + r2 + r0 + r3 + r0 + r4

    def tocsv(self):
        r0 = ','
        r1 = '"{0}"'.format(self.timestamp.encode('utf8'))
        r2 = '"{0}"'.format(self.type.encode('utf8'))
        r3 = '"{0}"'.format(self.orgId.encode('utf8'))
        r4 = '"{0}"'.format(self.recordId.encode('utf8'))
        r5 = '"{0}"'.format(self.userId.encode('utf8'))
        r6 = '"{0}"'.format(self.policyId.encode('utf8'))
        r7 = '"{0}"'.format(self.requestIp.encode('utf8'))
        r8 = '"{0}"'.format(self.virtruClient.encode('utf8'))
        r9 = '"{0}"'.format(self.created.encode('utf8'))
        r10 = '"{0}"'.format(self.requestId.encode('utf8'))
        r11 = '"{0}"'.format(self.orgActionType.encode('utf8'))
        r12 = '"{0}"'.format(self.lastModified.encode('utf8'))
        r13 = '"{0}"'.format(self.action.encode('utf8'))
        r14 = '"{0}"'.format(self.userAgent.encode('utf8'))
        r15 = '"{0}"'.format(self.isNoAuth)

        ra = r1 + r0 + r2 + r0 + r3 + r0 + r4 + r0 + r5 + r0 + r6 + r0 + r7 + r0 + r8 + r0 + r9 + r0 + r10 + r0
        rb = r11 + r0 + r12 + r0 + r13 + r0 + r14 + r0 + r15

        return ra + rb

    def tosyslog(self):
        r0 = ' '
        r1 = '"userId={}"'.format(self.userId.encode('utf8'))
        r2 = '"policyId={}"'.format(self.policyId.encode('utf8'))
        r3 = '"requestIp={}"'.format(self.requestIp.encode('utf8'))
        r4 = '"virtruClient={}"'.format(self.virtruClient.encode('utf8'))
        r5 = '"created={}"'.format(self.created.encode('utf8'))
        r6 = '"recordId={}"'.format(self.recordId.encode('utf8'))
        r7 = '"timestamp={}"'.format(self.timestamp.encode('utf8'))
        r8 = '"orgId={}"'.format(self.orgId.encode('utf8'))
        r9 = '"requestId={}"'.format(self.requestId.encode('utf8'))
        r10 = '"orgActionType={}"'.format(self.orgActionType.encode('utf8'))
        r11 = '"lastModified={}"'.format(self.lastModified.encode('utf8'))
        r12 = '"action={}"'.format(self.action.encode('utf8'))
        r13 = '"userAgent={}"'.format(self.userAgent.encode('utf8'))
        r14 = '"type={}"'.format(self.type.encode('utf8'))
        r15 = '"isNoAuth={}"'.format(self.isNoAuth)

        ra = r1 + r0 + r2 + r0 + r3 + r0 + r4 + r0 + r5 + r0 + r6 + r0 + r7 + r0 + r8 + r0 + r9 + r0 + r10 + r0
        rb = r11 + r0 + r12 + r0 + r13 + r0 + r14 + r0 + r15

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
