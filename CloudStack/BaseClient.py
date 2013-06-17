import urllib2
import urllib
import json
import hmac
import base64
import hashlib
import re
import sys, traceback

class BaseClient(object):
    def __init__(self, api, apikey, secret):
        self.api = api
        self.apikey = apikey
        self.secret = secret

    def request(self, command, args):
        args['apikey']   = self.apikey
        args['command']  = command
        args['response'] = 'json'
        
        params=[]
        
        keys = sorted(args.keys())

        for k in keys:
            params.append(k + '=' + urllib.quote_plus(args[k]).replace("+", "%20"))
       
        query = '&'.join(params)

        signature = base64.b64encode(hmac.new(
            self.secret, 
            msg=query.lower(), 
            digestmod=hashlib.sha1
        ).digest())

        query += '&signature=' + urllib.quote_plus(signature)

	try:
	        response = urllib2.urlopen(self.api + '?' + query)
	except urllib2.HTTPError as e:
		print e.code
	except urllib2.URLError as e:
		#print "URLError: ", e.args, e.reason, e.reason.errno
		#e = sys.exc_info()[0]
		#sys.exit(0)
		raise e
	except Exception:
		e = sys.exc_info()[0]
		print "ERROR: ", e
		sys.exit(0)
        decoded = json.loads(response.read())
       
        propertyResponse = command.lower() + 'response'
        if not propertyResponse in decoded:
            if 'errorresponse' in decoded:
                raise RuntimeError("ERROR: " + decoded['errorresponse']['errortext'])
            else:
                raise RuntimeError("ERROR: Unable to parse the response")

        response = decoded[propertyResponse]
        result = re.compile(r"^list(\w+)s").match(command.lower())

        if not result is None:
            type = result.group(1)

            if type in response:
                return response[type]
            else:
                # sometimes, the 's' is kept, as in :
                # { "listasyncjobsresponse" : { "asyncjobs" : [ ... ] } }
                type += 's'
                if type in response:
                    return response[type]

        return response
