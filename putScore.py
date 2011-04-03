import datetime

from google.appengine.ext import db
from google.appengine.ext import webapp

from Tapper import Tapper

class PutScoreHandler(webapp.RequestHandler):
	def get(self, uid, score):
		tapper = Tapper.get(uid)
		# query = db.GqlQuery("SELECT * FROM Tapper WHERE  = :1", long(uid))
		# tapper = query.get()
		if tapper:
			tapper.score = int(score)
			tapper.score_time = datetime.datetime.now()
			tapper.put()
