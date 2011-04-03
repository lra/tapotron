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

from Tapper import Tapper

import tools


def base64_url_decode(data):
	data = data.encode(u'ascii')
	data += '=' * (4 - (len(data) % 4))
	return base64.urlsafe_b64decode(data)

def get_fbuid_from_signed_request(signed_request):
	app_secret = '3343b1814e225d22b55a92cbb04c970f'

	try:
		sig, payload = signed_request.split(u'.', 1)
		sig = base64_url_decode(sig)
		data = json.loads(base64_url_decode(payload))
		
		expected_sig = hmac.new(app_secret, msg=payload, digestmod=hashlib.sha256).digest()

		# allow the signed_request to function for upto 1 day
		if sig == expected_sig and data[u'issued_at'] > (time.time() - 86400):
			fb_user_id = data.get(u'user_id')
	except ValueError, ex:
		pass # ignore if can't split on dot
	
	return fb_user_id

class MainHandler(webapp.RequestHandler):

	app_id = '152524664810770'
	test_uid = 123
	passed = False
	fb_user_id = None

	def get(self):
		if tools.on_dev_server():
			self.display_index(self.test_uid)

	def post(self):
		signed_request = cgi.escape(self.request.get('signed_request'))
		fb_uid = get_fbuid_from_signed_request(signed_request)
		self.display_index(fb_uid)
	
	def display_index(self, fb_uid):
		if not fb_uid:
			install_url = 'https://www.facebook.com/dialog/oauth?client_id='+self.app_id+'&redirect_uri=http://apps.facebook.com/tapotron/'
			install_html = '<html><body><script type="text/javascript">parent.location.href="'+install_url+'";</script></body></html>'
			self.response.out.write(install_html)
		else:
			query = db.GqlQuery("SELECT * FROM Tapper WHERE facebook_uid = :1", long(fb_uid))
			tapper = query.get()
			if not tapper:
				tapper = Tapper(facebook_uid = long(fb_uid))
				self.response.out.write('New user!')
			tapper.put()
			template_values = {'uid': tapper.key()}
			path = 'templates/index.html'
			self.response.out.write(template.render(path, template_values))
