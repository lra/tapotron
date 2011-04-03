import cgi

from google.appengine.ext import webapp


class MainHandler(webapp.RequestHandler):

    def get(self):
        self.response.out.write('<html><body>GET You wrote:<pre>')
        self.response.out.write(cgi.escape(self.request.get('content')))
        self.response.out.write('</pre></body></html>')
        

    def post(self):
        self.response.out.write('<html><body>POST You wrote:<pre>')
        self.response.out.write(cgi.escape(self.request.get('content')))
        self.response.out.write('</pre></body></html>')
