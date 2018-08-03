class UnitAttributes:

    def __init__(self):
        self.adminPolicyEdit = []
        self.orgActionType = ''
        self.unitType = ''
        self.adminPolicyContractFetch = []
        self.adminDlp = []
        self.userAgent = ''
        self.requestIp = ''
        self.recordId = ''
        self.requestId = ''
        self.type = ''
        self.virtruClient = ''
        self.adminPolicyBulkExport = []
        self.timestamp = ''
        self.adminPolicyRead = []
        self.adminUnit = []
        self.permissions = []
        self.remoteId = ''
        self.name = ''
        self.created = ''
        self.lastModified = ''
        self.orgId = ''
        self.action = ''
        self.adminPolicyRevoke = []

    def loadjson(self, jsonin):
        self.adminPolicyEdit = jsonin.get('adminPolicyEdit', None)
        self.orgActionType = jsonin.get('orgActionType', '')
        self.unitType = jsonin.get('unitType', '')
        self.adminPolicyContractFetch = jsonin.get('adminPolicyContractFetch', None)
        self.adminDlp = jsonin.get('adminDlp', None)
        self.userAgent = jsonin.get('userAgent', '')
        self.requestIp = jsonin.get('requestIp', '')
        self.recordId = jsonin.get('recordId', '')
        self.requestId = jsonin.get('requestId', '')
        self.type = jsonin.get('type', '')
        self.virtruClient = jsonin.get('virtruClient', '')
        self.adminPolicyBulkExport = jsonin.get('adminPolicyBulkExport', None)
        self.timestamp = jsonin.get('timestamp', '')
        self.adminPolicyRead = jsonin.get('adminPolicyRead', None)
        self.adminUnit = jsonin.get('adminUnit', None)
        self.permissions = jsonin.get('permissions', None)
        self.remoteId = jsonin.get('remoteId', '')
        self.name = jsonin.get('name', '')
        self.created = jsonin.get('created', '')
        self.lastModified = jsonin.get('lastModified', '')
        self.orgId = jsonin.get('orgId', '')
        self.action = jsonin.get('action', '')
        self.adminPolicyRevoke = jsonin.get('adminPolicyRevoke', None)

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
        r5 = '"{0}"'.format(self.flatten(self.adminPolicyEdit))
        r6 = '"{0}"'.format(self.orgActionType.encode('utf8'))
        r7 = '"{0}"'.format(self.unitType.encode('utf8'))
        r8 = '"{0}"'.format(self.flatten(self.adminPolicyContractFetch))
        r9 = '"{0}"'.format(self.flatten(self.adminDlp))
        r10 = '"{0}"'.format(self.userAgent.encode('utf8'))
        r11 = '"{0}"'.format(self.requestIp.encode('utf8'))
        r12 = '"{0}"'.format(self.requestId.encode('utf8'))
        r13 = '"{0}"'.format(self.virtruClient.encode('utf8'))
        r14 = '"{0}"'.format(self.flatten(self.adminPolicyBulkExport))
        r15 = '"{0}"'.format(self.flatten(self.adminPolicyRead))
        r16 = '"{0}"'.format(self.flatten(self.adminUnit))
        r17 = '"{0}"'.format(self.flatten(self.permissions))
        r18 = '"{0}"'.format(self.remoteId.encode('utf8'))
        r19 = '"{0}"'.format(self.name.encode('utf8'))
        r20 = '"{0}"'.format(self.created.encode('utf8'))
        r21 = '"{0}"'.format(self.lastModified.encode('utf8'))
        r22 = '"{0}"'.format(self.action.encode('utf8'))
        r23 = '"{0}"'.format(self.adminPolicyRevoke)

        ra = r1 + r0 + r2 + r0 + r3 + r0 + r4 + r0 + r5 + r0 + r6 + r0 + r7 + r0 + r8 + r0 + r9 + r0 + r10 + r0
        rb = r11 + r0 + r12 + r0 + r13 + r0 + r14 + r0 + r15 + r0 + r16 + r0 + r17 + r0 + r18 + r0 + r19 + r0 + r20 + r0
        rc = r21 + r0 + r22 + r0 + r23

        return ra + rb + rc

    def tosyslog(self):
        r0 = ' '
        r1 = '"adminPolicyEdit={0}"'.format(self.flatten(self.adminPolicyEdit))
        r2 = '"orgActionType={0}"'.format(self.orgActionType.encode('utf8'))
        r3 = '"unitType={0}"'.format(self.unitType.encode('utf8'))
        r4 = '"adminPolicyContractFetch={0}"'.format(self.flatten(self.adminPolicyContractFetch))
        r5 = '"adminDlp={0}"'.format(self.flatten(self.adminDlp))
        r6 = '"userAgent={0}"'.format(self.userAgent.encode('utf8'))
        r7 = '"requestIp={0}"'.format(self.requestIp.encode('utf8'))
        r8 = '"recordId={0}"'.format(self.recordId.encode('utf8'))
        r9 = '"requestId={0}"'.format(self.requestId.encode('utf8'))
        r10 = '"type={0}"'.format(self.type.encode('utf8'))
        r11 = '"virtruClient={0}"'.format(self.virtruClient.encode('utf8'))
        r12 = '"adminPolicyBulkExport={0}"'.format(self.flatten(self.adminPolicyBulkExport))
        r13 = '"timestamp={0}"'.format(self.timestamp.encode('utf8'))
        r14 = '"adminPolicyRead={0}"'.format(self.flatten(self.adminPolicyRead))
        r15 = '"adminUnit={0}"'.format(self.flatten(self.adminUnit))
        r16 = '"permissions={0}"'.format(self.flatten(self.permissions))
        r17 = '"remoteId={0}"'.format(self.remoteId.encode('utf8'))
        r18 = '"name={0}"'.format(self.name.encode('utf8'))
        r19 = '"created={0}"'.format(self.created.encode('utf8'))
        r20 = '"lastModified={0}"'.format(self.lastModified.encode('utf8'))
        r21 = '"orgId={0}"'.format(self.orgId.encode('utf8'))
        r22 = '"action={0}"'.format(self.action.encode('utf8'))
        r23 = '"adminPolicyRevoke={0}"'.format(self.flatten(self.adminPolicyRevoke))

        ra = r1 + r0 + r2 + r0 + r3 + r0 + r4 + r0 + r5 + r0 + r6 + r0 + r7 + r0 + r8 + r0 + r9 + r0 + r10 + r0
        rb = r11 + r0 + r12 + r0 + r13 + r0 + r14 + r0 + r15 + r0 + r16 + r0 + r17 + r0 + r18 + r0 + r19 + r0 + r20 + r0
        rc = r21 + r0 + r22 + r0 + r23

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
