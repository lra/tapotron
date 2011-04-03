class GetScoreUidHandler(webapp.RequestHandler):
    def get(self, uid):
        self.response.out.write('Get someone\'s score')
