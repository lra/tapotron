from google.appengine.ext import webapp

from Tapper import Tapper


class GetScoreHandler(webapp.RequestHandler):
	def get(self, uid):
		score = 0

		try:
			tapper = Tapper.get(uid)
			if tapper:
				if tapper.score:
					score = tapper.score
		except:
			pass

		self.response.out.write(str(score))
