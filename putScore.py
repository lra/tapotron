import datetime

from google.appengine.ext import db
from google.appengine.ext import webapp

from Tapper import Tapper


class PutScoreHandler(webapp.RequestHandler):
	def get(self, uid, score):
		saved = False
		try:
			tapper = Tapper.get(uid)
			if tapper:
				new_score = int(score)
				if new_score > tapper.score:
					tapper.score = int(score)
					tapper.score_time = datetime.datetime.now()
					tapper.put()
					saved = True
		except:
			pass

		if saved:
			self.response.out.write('1')
		else:
			self.response.out.write('0')
