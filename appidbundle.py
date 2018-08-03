class AppIdBundle:

    def __init__(self):
        self.requestIp = ''
        self.virtruClient = ''
        self.created = ''
        self.recordId = ''
        self.timestamp = ''
        self.userId = ''
        self.orgId = ''
        self.primaryOu = ''
        self.isRevokedEvent = False
        self.ous = []
        self.state = ''
        self.orgActionType = ''
        self.requestId = ''
        self.groups = []
        self.lastModified = ''
        self.action = ''
        self.userAgent = ''
        self.isDisableEvent = False
        self.type = ''
        self.isActivateEvent = False

    def loadjson(self, jsonin):

        self.requestIp = jsonin.get('requestIp', '')
        self.virtruClient = jsonin.get('virtruClient', '')
        self.created = jsonin.get('created', '')
        self.recordId = jsonin.get('recordId', '')
        self.timestamp = jsonin.get('timestamp', '')
        self.userId = jsonin.get('userId', '')
        self.orgId = jsonin.get('orgId', '')
        self.primaryOu = jsonin.get('primaryOu', '')
        self.isRevokedEvent = jsonin.get('isRevokedEvent', False)
        self.ous = jsonin.get('ous', None)
        self.state = jsonin.get('state', '')
        self.orgActionType = jsonin.get('orgActionType', '')
        self.requestId = jsonin.get('requestId', '')
        self.groups = jsonin.get('groups', None)
        self.lastModified = jsonin.get('lastModified', '')
        self.action = jsonin.get('action', '')
        self.userAgent = jsonin.get('userAgent', '')
        self.isDisableEvent = jsonin.get('isDisableEvent', False)
        self.type = jsonin.get('type', '')
        self.isActivateEvent = jsonin.get('isActivateEvent', False)

    def __str__(self):
        r0 = ','
        r1 = '"{0}"'.format(self.timestamp.encode('utf8'))
        r2 = '"{0}"'.format(self.type.encode('utf8'))
        r3 = '"{0}"'.format(self.orgId.encode('utf8'))
        r4 = '"{0}"'.format(self.recordId).encode('utf8')
        return r1 + r0 + r2 + r0 + r3 + r0 + r4

    def tocsv(self):
        r0 = ','
        r1 = '"{0}"'.format(self.timestamp.encode('utf8'))
        r2 = '"{0}"'.format(self.type.encode('utf8'))
        r3 = '"{0}"'.format(self.orgId).encode('utf8')
        r4 = '"{0}"'.format(self.recordId.encode('utf8'))
        r5 = '"{0}"'.format(self.requestIp.encode('utf8'))
        r6 = '"{0}"'.format(self.virtruClient.encode('utf8'))
        r7 = '"{0}"'.format(self.created.encode('utf8'))
        r8 = '"{0}"'.format(self.userId.encode('utf8'))
        r9 = '"{0}"'.format(self.primaryOu.encode('utf8'))
        r10 = '"{0}"'.format(self.flatten(self.ous))
        r11 = '"{0}"'.format(self.isRevokedEvent)
        r12 = '"{0}"'.format(self.isActivateEvent)
        r13 = '"{0}"'.format(self.state.encode('utf8'))
        r14 = '"{0}"'.format(self.orgActionType.encode('utf8'))
        r15 = '"{0}"'.format(self.requestId.encode('utf8'))
        r16 = '"{0}"'.format(self.flatten(self.groups))
        r17 = '"{0}"'.format(self.lastModified.encode('utf8'))
        r18 = '"{0}"'.format(self.action.encode('utf8'))
        r19 = '"{0}"'.format(self.userAgent.encode('utf8'))
        r20 = '"{0}"'.format(self.isDisableEvent)

        ra = r1 + r0 + r2 + r0 + r3 + r0 + r4 + r0 + r5 + r0 + r6 + r0 + r7 + r0 + r8 + r0 + r9 + r0 + r10 + r0
        rb = r11 + r0 + r12 + r0 + r13 + r0 + r14 + r0 + r15 + r0 + r16 + r0 + r17 + r0 + r18 + r0 + r19 + r0 + r20

        return ra + rb

    def tosyslog(self):
        r0 = ' '
        r1 = '"requestIp={}"'.format(self.requestIp.encode('utf8'))
        r2 = '"virtruClient={}"'.format(self.virtruClient.encode('utf8'))
        r3 = '"created={}"'.format(self.created.encode('utf8'))
        r4 = '"recordId={}"'.format(self.recordId.encode('utf8'))
        r5 = '"timestamp={}"'.format(self.timestamp.encode('utf8'))
        r6 = '"userId={}"'.format(self.userId.encode('utf8'))
        r7 = '"orgId={}"'.format(self.orgId.encode('utf8'))
        r8 = '"primaryOu={}"'.format(self.primaryOu.encode('utf8'))
        r9 = '"isRevokedEvent={}"'.format(self.isRevokedEvent)
        r10 = '"ous={}"'.format(self.flatten(self.ous))
        r11 = '"state={}"'.format(self.state.encode('utf8'))
        r12 = '"orgActionType={}"'.format(self.orgActionType.encode('utf8'))
        r13 = '"requestIdformat={}"'.format(self.requestId.encode('utf8'))
        r14 = '"groups={}"'.format(self.flatten(self.groups))
        r15 = '"lastModified={}"'.format(self.lastModified.encode('utf8'))
        r16 = '"action={}'.format(self.action.encode('utf8'))
        r17 = '"userAgent={}"'.format(self.userAgent.encode('utf8'))
        r18 = '"isDisableEvent={}"'.format(self.isDisableEvent)
        r19 = '"type={}"'.format(self.type.encode('utf8'))
        r20 = '"isActivateEvent={}"'.format(self.isActivateEvent)

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
