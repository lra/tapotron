import cgi
import base64
import hashlib
import hmac
import time


from google.appengine.ext import webapp

from django.utils import simplejson as json

def base64_url_decode(data):
    data = data.encode(u'ascii')
    data += '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data)

class MainHandler(webapp.RequestHandler):

    app_secret = '3343b1814e225d22b55a92cbb04c970f'

    def get(self):
        self.response.out.write('<html><body>GET You wrote:<pre>')
        self.response.out.write(cgi.escape(self.request.get('content')))
        self.response.out.write('</pre></body></html>')
        

    def post(self):
        signed_request = cgi.escape(self.request.get('signed_request'))
        try:
            sig, payload = signed_request.split(u'.', 1)
            sig = base64_url_decode(sig)
            data = json.loads(base64_url_decode(payload))

            expected_sig = hmac.new(
                self.app_secret, msg=payload, digestmod=hashlib.sha256).digest()

            # allow the signed_request to function for upto 1 day
            if sig == expected_sig and \
                    data[u'issued_at'] > (time.time() - 86400):
                self.signed_request = data
                self.user_id = data.get(u'user_id')
                self.access_token = data.get(u'oauth_token')
        except ValueError, ex:
            pass # ignore if can't split on dot
            
        self.response.out.write('<html><body>POST You wrote:<pre>')
        self.response.out.write(self.user_id)
        self.response.out.write('</pre></body></html>')

