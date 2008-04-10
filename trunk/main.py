import wsgiref.handlers
import uuid
from google.appengine.api import users 
from google.appengine.ext import webapp
from pastebin import Site
from paste import Paste

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        self.response.headers['Content-Type'] = 'text/html'
        if user:
            self.response.out.write(Site(self, user.nickname()).getContent())
        else:
            self.response.out.write(Site(self, 'anonymous').getContent())

    
    def post(self):

        user = users.get_current_user()

        #XXX: needs validation!

        paste = Paste()

        paste.uid = "p" + str(uuid.uuid4())[:8]
        if user:
            paste.userid = user.nickname()
        else:
            paste.userid = "anonymous"

        paste.title = self.request.get("title")
        paste.comment = self.request.get("comment")
        paste.code = self.request.get("code")
        paste.put()

        self.response.headers['Content-Type'] = 'text/html'
        if user:
            self.response.out.write(Site(self, user.nickname()).getContent(uid=paste.uid))
        else:
            self.response.out.write(Site(self, 'anonymous').getContent(uid=paste.uid))


def main():
    application = webapp.WSGIApplication([('/.*', MainPage)], debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
