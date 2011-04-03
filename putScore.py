from google.appengine.ext import webapp

class PutScoreHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Put a new score')
