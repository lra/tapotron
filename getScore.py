from google.appengine.ext import webapp

class GetScoreHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Get my own score')
