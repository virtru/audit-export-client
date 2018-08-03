class Policy:

    def __init__(self):
        self.orgActionType = ''
        self.userId = ''
        self.isRevokeEvent = ''
        self.ous = []
        self.userAgent = ''
        self.requestIp = ''
        self.recordId = ''
        self.isForwardingDisabled = False
        self.state = ''
        self.requestId = ''
        self.isExpireEvent = False
        self.type = ''
        self.violatedRuleIds = []
        self.virtruClient = ''
        self.recipients = []
        self.timestamp = ''
        self.primaryOu = ''
        self.isManaged = False
        self.policyType = ''
        self.groups = []
        self.isNoAuth = None
        self.displayName = ''
        self.isManagedEvent = False
        self.lastModified = ''
        self.created = ''
        self.orgId = ''
        self.policyId = ''
        self.action = ''
        self.isNoAuthEvent = False
        self.isForwardingDisabledEvent = False

    def loadjson(self, jsonin):
        self.orgActionType = jsonin.get('orgActionType', '')
        self.userId = jsonin.get('userId', '')
        self.isRevokeEvent = jsonin.get('isRevokeEvent', False)
        self.ous = jsonin.get('ous', None)
        self.userAgent = jsonin.get('userAgent', '')
        self.requestIp = jsonin.get('requestIp', '')
        self.recordId = jsonin.get('recordId', '')
        self.isForwardingDisabled = jsonin.get('isForwardingDisabled', False)
        self.state = jsonin.get('state', '')
        self.requestId = jsonin.get('requestId', '')
        self.isExpireEvent = jsonin.get('isExpireEvent', False)
        self.type = jsonin.get('type', '')
        self.violatedRuleIds = jsonin.get('violatedRuleIds', None)
        self.virtruClient = jsonin.get('virtruClient', '')
        self.recipients = jsonin.get('recipients', None)
        self.timestamp = jsonin.get('timestamp', '')
        self.primaryOu = jsonin.get('primaryOu', '')
        self.isManaged = jsonin.get('isManaged', False)
        self.policyType = jsonin.get('policyType', '')
        self.groups = jsonin.get('groups', None)
        self.isNoAuth = jsonin.get('isNoAuth', False)
        self.displayName = jsonin.get('displayName', '')
        self.isManagedEvent = jsonin.get('isManagedEvent', False)
        self.lastModified = jsonin.get('lastModified', '')
        self.created = jsonin.get('created', '')
        self.orgId = jsonin.get('orgId', '')
        self.policyId = jsonin.get('policyId', '')
        self.action = jsonin.get('action', '')
        self.isNoAuthEvent = jsonin.get('isNoAuthEvent', False)
        self.isForwardingDisabledEvent = jsonin.get('isForwardingDisabledEvent', False)

    def __str__(self):
        r0 = ','
        r1 = '"{0}"'.format(self.timestamp.encode('utf8'))
        r2 = '"{0}"'.format(self.type.encode('utf8'))
        r3 = '"{0}"'.format(self.orgId.encode('utf8'))
        r4 = '"{0}"'.format(self.recordId.encode('utf8'))
        return r1 + r0 + r2 + r0 + r3 + r0 + r4

    def tocsv(self):
        r0 = ','
        r1 = '"{0}"'.format(self.orgActionType.encode('utf8'))
        r2 = '"{0}"'.format(self.userId.encode('utf8'))
        r3 = '"{0}"'.format(self.isRevokeEvent)
        r4 = '"{0}"'.format(self.flatten(self.ous))
        r5 = '"{0}"'.format(self.userAgent.encode('utf8'))
        r6 = '"{0}"'.format(self.requestIp.encode('utf8'))
        r7 = '"{0}"'.format(self.recordId.encode('utf8'))
        r8 = '"{0}"'.format(self.isForwardingDisabled)
        r9 = '"{0}"'.format(self.state.encode('utf8'))
        r10 = '"{0}"'.format(self.requestId.encode('utf8'))
        r11 = '"{0}"'.format(self.isExpireEvent)
        r12 = '"{0}"'.format(self.type.encode('utf8'))
        r13 = '"{0}"'.format(self.flatten(self.violatedRuleIds))
        r14 = '"{0}"'.format(self.virtruClient.encode('utf8'))
        r15 = '"{0}"'.format(self.flatten(self.recipients))
        r16 = '"{0}"'.format(self.timestamp.encode('utf8'))
        r17 = '"{0}"'.format(self.primaryOu.encode('utf8'))
        r18 = '"{0}"'.format(self.isManaged)
        r19 = '"{0}"'.format(self.policyType.encode('utf8'))
        r20 = '"{0}"'.format(self.flatten(self.groups))
        r21 = '"{0}"'.format(self.isNoAuth)
        r22 = '"{0}"'.format(self.displayName.encode('utf8'))
        r23 = '"{0}"'.format(self.isManagedEvent)
        r24 = '"{0}"'.format(self.lastModified.encode('utf8'))
        r25 = '"{0}"'.format(self.created.encode('utf8'))
        r26 = '"{0}"'.format(self.orgId.encode('utf8'))
        r27 = '"{0}"'.format(self.policyId.encode('utf8'))
        r28 = '"{0}"'.format(self.action.encode('utf8'))
        r29 = '"{0}"'.format(self.isNoAuthEvent)
        r30 = '"{0}"'.format(self.isForwardingDisabledEvent)

        ra = r1 + r0 + r2 + r0 + r3 + r0 + r4 + r0 + r5 + r0 + r6 + r0 + r7 + r0 + r8 + r0 + r9 + r0 + r10 + r0
        rb = r11 + r0 + r12 + r0 + r13 + r0 + r14 + r0 + r15 + r0 + r16 + r0 + r17 + r0 + r18 + r0 + r19 + r0 + r20 + r0
        rc = r21 + r0 + r22 + r0 + r23 + r0 + r24 + r0 + r25 + r0 + r26 + r0 + r27 + r0 + r28 + r0 + r29 + r0 + r30

        return ra + rb + rc

    def tosyslog(self):
        r0 = ' '
        r1 = '"orgActionType={0}"'.format(self.orgActionType.encode('utf8'))
        r2 = '"userId={0}"'.format(self.userId.encode('utf8'))
        r3 = '"isRevokeEvent={0}"'.format(self.isRevokeEvent)
        r4 = '"ous={0}"'.format(self.flatten(self.ous))
        r5 = '"userAgent={0}"'.format(self.userAgent.encode('utf8'))
        r6 = '"requestIp={0}"'.format(self.requestIp.encode('utf8'))
        r7 = '"recordId={0}"'.format(self.recordId.encode('utf8'))
        r8 = '"isForwardingDisabled={0}"'.format(self.isForwardingDisabled)
        r9 = '"state={0}"'.format(self.state.encode('utf8'))
        r10 = '"requestId={0}"'.format(self.requestId.encode('utf8'))
        r11 = '"isExpireEvent={0}"'.format(self.isExpireEvent)
        r12 = '"type={0}"'.format(self.type.encode('utf8'))
        r13 = '"violatedRuleIds={0}"'.format(self.flatten(self.violatedRuleIds))
        r14 = '"virtruClient={0}"'.format(self.virtruClient.encode('utf8'))
        r15 = '"recipients={0}"'.format(self.flatten(self.recipients))
        r16 = '"timestamp={0}"'.format(self.timestamp.encode('utf8'))
        r17 = '"primaryOu={0}"'.format(self.primaryOu.encode('utf8'))
        r18 = '"isManaged={0}"'.format(self.isManaged)
        r19 = '"policyType={0}"'.format(self.policyType.encode('utf8'))
        r20 = '"groups={0}"'.format(self.flatten(self.groups))
        r21 = '"isNoAuth={0}"'.format(self.isNoAuth)
        r22 = '"displayName={0}"'.format(self.displayName.encode('utf8'))
        r23 = '"isManagedEvent={0}"'.format(self.isManagedEvent)
        r24 = '"lastModified={0}"'.format(self.lastModified.encode('utf8'))
        r25 = '"created={0}"'.format(self.created.encode('utf8'))
        r26 = '"orgId={0}"'.format(self.orgId.encode('utf8'))
        r27 = '"policyId={0}"'.format(self.policyId.encode('utf8'))
        r28 = '"action={0}"'.format(self.action.encode('utf8'))
        r29 = '"isNoAuthEvent={0}"'.format(self.isNoAuthEvent)
        r30 = '"isForwardingDisabledEvent={0}"'.format(self.isForwardingDisabledEvent)

        ra = r1 + r0 + r2 + r0 + r3 + r0 + r4 + r0 + r5 + r0 + r6 + r0 + r7 + r0 + r8 + r0 + r9 + r0 + r10 + r0
        rb = r11 + r0 + r12 + r0 + r13 + r0 + r14 + r0 + r15 + r0 + r16 + r0 + r17 + r0 + r18 + r0 + r19 + r0 + r20 + r0
        rc = r21 + r0 + r22 + r0 + r23 + r0 + r24 + r0 + r25 + r0 + r26 + r0 + r27 + r0 + r28 + r0 + r29 + r0 + r30

        return ra + rb + rc

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
