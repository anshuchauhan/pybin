import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from paste import Paste

class Feed(webapp.RequestHandler):
    def get_feeds(self,user):
        
        if user:
            user_feeds = db.GqlQuery("SELECT * FROM Paste WHERE name = :1 ORDER BY date DESC",user)
        else:
            user_feeds = db.GqlQuery("SELECT * FROM Paste ORDER BY date DESC")

        return user_feeds.fetch(10)

    def get(self):
        user = self.request.path.split('\n')
        user = user[0].split('f/')[1]
        aux = {}
        aux['feeds'] = self.get_feeds(user=user)

        return self.response.out.write(template.render("templates/feed.xml", aux))
        

def main():
    application = webapp.WSGIApplication([('/.*', Feed)], debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
