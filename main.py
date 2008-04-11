import wsgiref.handlers
import uuid
from google.appengine.api import users
from google.appengine.ext import webapp
from pastebin import Site

class MainPage(webapp.RequestHandler):

    def __init__(self):
        """ Getting the user information so we can use it in the whole website. """
        user = users.get_current_user()
            
        if user:
            url = users.create_logout_url("/")
            logmessage = ""
            url_linktext = 'Logout'
            user = user.nickname()
        else:
            url = users.create_login_url("/")
            logmessage = "You can "
            url_linktext = 'Login using your Google Account'
            user = 'anonymous'
	
        self.user_status_values = {
              'message': logmessage,
              'url_login': url,
              'url_linktext': url_linktext,
              'user': user,
              }

	  

    
    def get(self):
        
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(Site(self, self.user_status_values).get_content())

      
    def post(self):
        
        from paste import Paste
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

        paste = Paste()
        #getting only the first 8 characters of uuid:
        paste.uid = str(uuid.uuid4())[:8]
        paste.name = self.user_status_values['user']
        paste.title = val.get_var("title")
        paste.comment = val.get_var("comment")
        paste.code = val.get_var("code")
        paste.type = val.get_var("type")
        paste.put()

        self.response.headers['Content-Type'] = 'text/html'
        write(Site(self, self.user_status_values).get_content(uid=paste.uid))
        
            
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
