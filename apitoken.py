class ApiToken:

    def __init__(self):
        self.displayName = ''
        self.creator = ''
        self.recordId = ''
        self.lastModified = ''
        self.tokenId = ''
        self.created = ''
        self.owner = ''
        self.orgId = ''
        self.orgActionType = ''
        self.timestamp = ''
        self.action = ''
        self.type = ''
        self.permissions = []

    def loadjson(self, jsonin):
        self.displayName = jsonin.get('displayName', '')
        self.creator = jsonin.get('creator', '')
        self.recordId = jsonin.get('recordId', '')
        self.lastModified = jsonin.get('lastModified', '')
        self.tokenId = jsonin.get('tokenId', '')
        self.created = jsonin.get('created', '')
        self.owner = jsonin.get('owner', '')
        self.orgId = jsonin.get('orgId', '')
        self.orgActionType = jsonin.get('orgActionType', '')
        self.timestamp = jsonin.get('timestamp', '')
        self.action = jsonin.get('action', '')
        self.type = jsonin.get('type', '')
        self.permissions = jsonin.get('permissions', None)
        self.tenantId = jsonin.get('tenant')

    def __str__(self):
        r0 = ','
        r1 = '"{0}"'.format(self.timestamp.encode('utf8'))
        r2 = '"{0}"'.format(self.type.encode('utf8'))
        r3 = '"{0}"'.format(self.orgId.encode('utf8'))
        r4 = '"{0}"'.format(self.recordId.encode('utf8'))
        return r1+r0+r2+r0+r3+r0+r4

    def tocsv(self):
        r0 = ','
        r1 = '"{0}"'.format(self.timestamp.encode('utf8'))
        r2 = '"{0}"'.format(self.type.encode('utf8'))
        r3 = '"{0}"'.format(self.orgId.encode('utf8'))
        r4 = '"{0}"'.format(self.recordId.encode('utf8'))
        r5 = '"{0}"'.format(self.displayName.encode('utf8'))
        r6 = '"{0}"'.format(self.creator.encode('utf8'))
        r7 = '"{0}"'.format(self.lastModified.encode('utf8'))
        r8 = '"{0}"'.format(self.tokenId.encode('utf8'))
        r9 = '"{0}"'.format(self.created.encode('utf8'))
        r10 = '"{0}"'.format(self.owner.encode('utf8'))
        r11 = '"{0}"'.format(self.orgActionType.encode('utf8'))
        r12 = '"{0}"'.format(self.action.encode('utf8'))
        r13 = '"{0}"'.format(self.flatten(self.permissions))

        ra = r1+r0+r2+r0+r3+r0+r4+r0+r5+r0+r6+r0+r7+r0+r8+r0+r9+r0+r10
        rb = r0+r11+r0+r12+r0+r13
        return ra+rb

    def tosyslog(self):
        r0 = ' '
        r1 = '"displayName={0}"'.format(self.displayName.encode('utf8'))
        r2 = '"creator={0}"'.format(self.creator.encode('utf8'))
        r3 = '"recordId={0}"'.format(self.recordId.encode('utf8'))
        r4 = '"lastModified={0}"'.format(self.lastModified.encode('utf8'))
        r5 = '"tokenId={0}"'.format(self.tokenId.encode('utf8'))
        r6 = '"created={0}"'.format(self.created.encode('utf8'))
        r7 = '"owner={0}"'.format(self.owner.encode('utf8'))
        r8 = '"orgId={0}"'.format(self.orgId.encode('utf8'))
        r9 = '"orgActionType={0}"'.format(self.orgActionType.encode('utf8'))
        r10 = '"timestamp={0}"'.format(self.timestamp.encode('utf8'))
        r11 = '"action={0}"'.format(self.action.encode('utf8'))
        r12 = '"type={0}"'.format(self.type.encode('utf8'))
        r13 = '"permissions={0}"'.format(self.flatten(self.permissions))

        return r1+r0+r2+r0+r3+r0+r4+r0+r5+r0+r6+r0+r7+r0+r8+r0+r9+r0+r10+r0+r11+r0+r12+r0+r13

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
