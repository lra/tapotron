class GetScoreHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Get my own score')
