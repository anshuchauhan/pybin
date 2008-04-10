import wsgiref.handlers
import uuid
from google.appengine.api import users 
from google.appengine.ext import webapp
from pastebin import Site

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        self.response.headers['Content-Type'] = 'text/html'
        if user:
            self.response.out.write(Site(self, user.nickname()).getContent())
        else:
            self.response.out.write(Site(self, 'anonymous').getContent())

    
    def post(self):
        
        from paste import Paste
        from utils import Validator

        user = users.get_current_user()

        #XXX: needs validation!

        input = {
         "title": self.request.get("title"),
         "comment": self.request.get("comment"),
         "code": self.request.get("code")
        }

        val = Validator(input)

        if not val.isValid():
            self.response.out.write(
                Site(self, user.nickname()).getContent(notvalid=val.getIssues()), 
                vars=val.getVars()
            )
            return

        paste = Paste()

        #getting only the first 8 characters of uuid:
        paste.uid = str(uuid.uuid4())[:8]

        #XXX: need to add user interface
        if user:
            paste.userid = user.nickname()
        else:
            paste.userid = "anonymous"

        #XXX: need to add type 
        paste.title = val.getVar("title")
        paste.comment = val.getVar("comment")
        paste.code = val.getVar("code")
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
