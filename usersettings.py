class UserSettings:

    def __init__(self):
        self.created = ''
        self.recordId = ''
        self.lastModified = ''
        self.userId = ''
        self.primaryOu = ''
        self.ous = []
        self.orgActionType = ''
        self.groups = []
        self.timestamp = ''
        self.action = ''
        self.orgId = ''
        self.type = ''
        self.permissions = []

    def loadjson(self, jsonin):
        self.created = jsonin.get('created', '')
        self.recordId = jsonin.get('recordId', '')
        self.lastModified = jsonin.get('lastModified', '')
        self.userId = jsonin.get('userId', '')
        self.primaryOu = jsonin.get('primaryOu', '')
        self.ous = jsonin.get('ous', None)
        self.orgActionType = jsonin.get('orgActionType', '')
        self.groups = jsonin.get('groups', None)
        self.timestamp = jsonin.get('timestamp', '')
        self.action = jsonin.get('action', '')
        self.orgId = jsonin.get('orgId', '')
        self.type = jsonin.get('type', '')
        self.permissions = jsonin.get('permissions', None)

    def __str__(self):
        r0 = ','
        r1 = '"{0}"'.format(self.timestamp.encode('utf8'))
        r2 = '"{0}"'.format(self.type.encode('utf8'))
        r3 = '"{0}"'.format(self.orgId.encode('utf8'))
        r4 = '"{0}"'.format(self.recordId.encode('utf8'))

        return r1 + r0 + r2 + r0 + r3 + r0 + r4

    def tocsv(self):
        r0 = ','
        r1 = '"{0}"'.format(self.created.encode('utf8'))
        r2 = '"{0}"'.format(self.recordId.encode('utf8'))
        r3 = '"{0}"'.format(self.lastModified.encode('utf8'))
        r4 = '"{0}"'.format(self.userId.encode('utf8'))
        r5 = '"{0}"'.format(self.primaryOu.encode('utf8'))
        r6 = '"{0}"'.format(self.flatten(self.ous))
        r7 = '"{0}"'.format(self.orgActionType.encode('utf8'))
        r8 = '"{0}"'.format(self.flatten(self.groups))
        r9 = '"{0}"'.format(self.timestamp.encode('utf8'))
        r10 = '"{0}"'.format(self.action.encode('utf8'))
        r11 = '"{0}"'.format(self.orgId.encode('utf8'))
        r12 = '"{0}"'.format(self.type.encode('utf8'))
        r13 = '"{0}"'.format(self.flatten(self.permissions))

        ra = r1 + r0 + r2 + r0 + r3 + r0 + r4 + r0 + r5 + r0 + r6 + r0 + r7 + r0 + r8 + r0 + r9 + r0 + r10 + r0
        rb = r11 + r0 + r12 + r0 + r13

        return ra + rb

    def tosyslog(self):
        r0 = ' '
        r1 = '"created={0}"'.format(self.created.encode('utf8'))
        r2 = '"recordId={0}"'.format(self.recordId.encode('utf8'))
        r3 = '"lastModified={0}"'.format(self.lastModified.encode('utf8'))
        r4 = '"userId={0}"'.format(self.userId.encode('utf8'))
        r5 = '"primaryOu={0}"'.format(self.primaryOu.encode('utf8'))
        r6 = '"ous={0}"'.format(self.flatten(self.ous))
        r7 = '"orgActionType={0}"'.format(self.orgActionType.encode('utf8'))
        r8 = '"groups={0}"'.format(self.flatten(self.groups))
        r9 = '"timestamp={0}"'.format(self.timestamp.encode('utf8'))
        r10 = '"action={0}"'.format(self.action.encode('utf8'))
        r11 = '"orgId={0}"'.format(self.orgId.encode('utf8'))
        r12 = '"type={0}"'.format(self.type.encode('utf8'))
        r13 = '"permissions={0}"'.format(self.flatten(self.permissions))

        ra = r1 + r0 + r2 + r0 + r3 + r0 + r4 + r0 + r5 + r0 + r6 + r0 + r7 + r0 + r8 + r0 + r9 + r0 + r10 + r0
        rb = r11 + r0 + r12 + r0 + r13

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
