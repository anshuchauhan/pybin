import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from stats import Stats
from pbuser import Pbuser
from pbdb import Pbdb

class Statistics(webapp.RequestHandler):
    def __init__(self):
        """ Getting the user information so we can use it in the whole website. """

        self.curr_user = Pbuser(None)
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
        query = db.GqlQuery("SELECT * FROM Stats WHERE number >= 0 ORDER BY number DESC")
        aux = {}
        aux2 = []
        aux['stats'] = None
        for lang_stats in query:
            aux2.append(lang_stats)

        aux.update(self.user_status_values)
        aux['stats'] = aux2
        
        return self.response.out.write(template.render( "templates/stats.html" , aux ))


def main():
    application = webapp.WSGIApplication([('/.*', Statistics)], debug=True)
    wsgiref.handlers.CGIHandler().run(application)
