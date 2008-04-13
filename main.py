import wsgiref.handlers
import uuid
from google.appengine.ext import webapp
from google.appengine.ext import db
from pastebin import Site
from paste import Paste
from stats import Stats
from pbuser import Pbuser
from pbdb import Pbdb

class MainPage(webapp.RequestHandler):

    def __init__(self):
        """ Getting the user information so we can use it in the whole website. """

        self.db = Pbdb()
        self.db.paste = Paste()
        self.curr_user = Pbuser(self.db.paste)
        if self.curr_user.logged_in():
            logmessage = ""
            url_linktext = 'Logout'
        else:
            logmessage = "You can "
            url_linktext = 'login using your Google Account'
	
        self.user_status_values = {
              'message': logmessage,
              'url_login': self.curr_user.get_login_url(),
              'url_linktext': url_linktext,
              'user': self.curr_user.nickname(),
        }


    def get(self):
        
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(Site(self, self.user_status_values).get_content())

      
    def post(self):
        
        from utils import Validator

        #XXX: need to add user interface

        write = self.response.out.write

        #XXX: needs validation!

        input = {
         "title": self.request.get("title"),
         "comment": self.request.get("comment"),
         "code": self.request.get("code"),
         "type": self.request.get("type"),
        }

        val = Validator(input)

        if not val.is_valid():
            write(Site(self, self.user_status_values).get_content(issues=val.get_issues(),vars=val.get_vars())) 
            return

        #getting only the first 8 characters of uuid:
        self.db.paste.uid = str(uuid.uuid4())[:8]
        self.db.paste.name = self.user_status_values['user']
        self.db.paste.title = val.get_var("title")
        self.db.paste.comment = val.get_var("comment")
        self.db.paste.code = val.get_var("code")
        self.db.paste.type = val.get_var("type")
        self.db.paste.put()

        #Updating Type Statistics
        self.db.aux= db.GqlQuery("SELECT * FROM Stats WHERE type = :1",val.get_var("type")).fetch(1)

        if self.db.aux:
            for stat in self.db.aux:
                stat.number = stat.number+1
        else:
            stat = Stats(type=val.get_var("type"),number=1)

        stat.put()

        self.response.headers['Content-Type'] = 'text/html'
        write(Site(self, self.user_status_values).get_content(uid=self.db.paste.uid))
        
            
class Highlight(webapp.RequestHandler):

    """Used to get the syntax highlight css"""

    def get(self):
        from syntax import Syntax
        self.response.headers['Content-Type'] = 'text/css'
        self.response.out.write(Syntax.get_syntax_css())


def main():
    application = webapp.WSGIApplication([('/highlight.css', Highlight),('/.*', MainPage)], debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
