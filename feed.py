import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from paste import Paste

class Feed(webapp.RequestHandler):   
    def get_feeds(self,user):
        
        user_feeds = db.GqlQuery("SELECT * FROM Paste WHERE name = :1 ORDER BY date DESC",user)
        #need to check if paste is public. 
			
	real_feeds = user_feeds.fetch(10)
        return real_feeds

    def get(self):
        user = self.request.path.split('\n')
        user = user[0].split('f/')[1]
        aux = {}
        aux['user'] = user
        aux['feeds'] = self.get_feeds(user=user)

        return self.response.out.write(template.render( "templates/feed.xml" , aux))
        
        
def main():
    application = webapp.WSGIApplication([('/.*', Feed)], debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
