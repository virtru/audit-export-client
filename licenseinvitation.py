class LicenseInvitation:

    def __init__(self):
        self.invitationId = ''
        self.receiverId = ''
        self.created = ''
        self.status = ''
        self.acceptedOn = ''
        self.revokedOn = ''
        self.timestamp = ''
        self.type = ''
        self.orgId = ''
        self.recordId = ''

    def loadjson(self, jsonin):
        self.invitationId = jsonin.get('invitationId', '')
        self.receiverId = jsonin.get('receiverId', '')
        self.created = jsonin.get('created', '')
        self.status = jsonin.get('status', '')
        self.acceptedOn = jsonin.get('acceptedOn', '')
        self.revokedOn = jsonin.get('revokedOn', '')
        self.timestamp = jsonin.get('timestamp', '')
        self.type = jsonin.get('type', '')
        self.orgId = jsonin.get('orgId', '')
        self.recordId = jsonin.get('recordId', '')

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
        r5 = '"{0}"'.format(self.invitationId.encode('utf8'))
        r6 = '"{0}"'.format(self.receiverId.encode('utf8'))
        r7 = '"{0}"'.format(self.created.encode('utf8'))
        r8 = '"{0}"'.format(self.status.encode('utf8'))
        r9 = '"{0}"'.format(self.acceptedOn.encode('utf8'))
        r10 = '"{0}"'.format(self.revokedOn.encode('utf8'))
        
        ra = r1 + r0 + r2 + r0 + r3 + r0 + r4 + r0 + r5 + r0 + r6 + r0 + r7 + r0 + r8 + r0 + r9 + r0 + r10
      
        return ra

    def tosyslog(self):
        r0 = ' '
        r1 = '"invitationId={0}"'.format(self.invitationId.encode('utf8'))
        r2 = '"receiverId={0}"'.format(self.receiverId.encode('utf8'))
        r3 = '"created={0}"'.format(self.created.encode('utf8'))
        r4 = '"status={0}"'.format(self.status.encode('utf8'))
        r5 = '"acceptedOn={0}"'.format(self.acceptedOn.encode('utf8'))
        r6 = '"revokedOn={0}"'.format(self.revokedOn.encode('utf8'))
        r7 = '"timestamp={0}"'.format(self.timestamp.encode('utf8'))
        r8 = '"type={0}"'.format(self.type.encode('utf8'))
        r9 = '"orgId={0}"'.format(self.orgId.encode('utf8'))
        r10 = '"recordId={0}"'.format(self.recordId.encode('utf8'))

        ra = r1 + r0 + r2 + r0 + r3 + r0 + r4 + r0 + r5 + r0 + r6 + r0 + r7 + r0 + r8 + r0 + r9 + r0 + r10

        return ra

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
