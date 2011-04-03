import cgi
import base64
import hashlib
import hmac
import time
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from django.utils import simplejson as json

from google.appengine.ext import db


def base64_url_decode(data):
    data = data.encode(u'ascii')
    data += '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data)

class MainHandler(webapp.RequestHandler):

    app_secret = '3343b1814e225d22b55a92cbb04c970f'
    app_id = '152524664810770'
    passed = False
    fb_user_id = None

    def get(self):
        # self.response.out.write('<html><body>GET You wrote:<pre>')
        # self.response.out.write(cgi.escape(self.request.get('signed_request')))
        # self.response.out.write('</pre></body></html>')
        self.post()

    def post(self):
        signed_request = cgi.escape(self.request.get('signed_request'))

        try:
            sig, payload = signed_request.split(u'.', 1)
            sig = base64_url_decode(sig)
            data = json.loads(base64_url_decode(payload))

            expected_sig = hmac.new(
                self.app_secret, msg=payload, digestmod=hashlib.sha256).digest()

            # allow the signed_request to function for upto 1 day
            if sig == expected_sig and data[u'issued_at'] > (time.time() - 86400):
                self.passed = True
                self.signed_request = data
                self.fb_user_id = data.get(u'user_id')
                self.access_token = data.get(u'oauth_token')
        except ValueError, ex:
            pass # ignore if can't split on dot
        
        if not self.fb_user_id:
            install_url = 'https://www.facebook.com/dialog/oauth?client_id='+self.app_id+'&redirect_uri=http://apps.facebook.com/tapotron/'
            install_html = '<html><body><script type="text/javascript">parent.location.href="'+install_url+'";</script></body></html>'
            self.response.out.write(install_html)
        else:
			q = db.Query(Tapper).filter('facebook_uid =', self.fb_user_id)
			tapper = q.get()
			if not tapper:
				tapper = Tapper(facebook_uid=self.fb_user_id)
			tapper.put()
            template_values = {'uid': tapper.key()}
            path = 'templates/index.html'
            self.response.out.write(template.render(path, template_values))

            # self.response.out.write('<html><body>POST You wrote:<pre>')
            # self.response.out.write('Passed in if: '+str(self.passed))
            # self.response.out.write(str(self.fb_user_id))
            # self.response.out.write('</pre></body></html>')

