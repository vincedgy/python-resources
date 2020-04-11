#!/usr/bin/env python
import sys
import os
from flask import Flask
app = Flask(__name__)

ACTIVEMQ_CMD='/opt/activemq/bin/activemq query  --jmxurl service:jmx:rmi:///jndi/rmi://localhost:12346/jmxrmi  -QQueue=*  --view Name,QueueSize 2>/dev/null'

FAKE_RESULT = '''Name = ArchiveQueue
QueueSize = 0

Name = DLQ.EmailQueue
QueueSize = 82

Name = EmailQueue
QueueSize = 0

Name = WS.WsImportV3Queue
QueueSize = 0

Name = DLQ.ArchiveQueue
QueueSize = 76

Name = DLQ.DemandeQualifQueue
QueueSize = 819

Name = WS.WsImportFoQueue
QueueSize = 0

Name = DLQ.WS.WsImportFoQueueWS
QueueSize = 0

Name = DemandeQualifQueue
QueueSize = 0'''


def getActiveMQStatus():
    #result = os.popen(ACTIVEMQ_CMD).read()
    result = FAKE_RESULT
    response = '['
    content = ''
    for line in result.split('\n'):
        X = line.split('=')
        if X[0].strip() == 'Name':
            if content != '':
                content += ','
            content += '{"queue":"' + X[1].strip() + '",'
        else:
            if X[0].strip() == 'QueueSize':
                content += '"size":"' + X[1].strip() + '"}'
    response += content + ']'
    return response

@app.route("/")
def hello():
    return getActiveMQStatus()

def app_main():
    print 'Starting...'
    print getActiveMQStatus()

# -----------------------------------------------------------------
# Main call
if __name__ == '__main__':
    app_main()
