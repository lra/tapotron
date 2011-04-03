from google.appengine.ext import webapp


class debug(webapp.RequestHandler):
	def get(self):
		self.response.out.write('Debug')
