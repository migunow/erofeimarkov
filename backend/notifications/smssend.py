#coding: utf-8

import urllib
import urllib2

USER = 'stainful@gmail.com'
APIKEY = "ocSsSZ"
SENDER = 'EROFEI'
apiurl = "https://littlesms.ru/api/message/send"


def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict


def sendsms(recipients, message):
    values = {
        'user': USER,
        'sender': SENDER,
        'apikey': APIKEY,
        'recipients': recipients,
        'message': message
    }
    data = urllib.urlencode(encoded_dict(values))
    req = urllib2.Request(apiurl, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page