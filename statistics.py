import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from stats import Stats

class Statistics(webapp.RequestHandler):
    def get(self):
        query = db.GqlQuery("SELECT * FROM Stats WHERE number >= 0 ORDER BY number DESC")
        aux = {}
        aux2 = []
        aux['stats'] = None
        for lang_stats in query:
            aux2.append(lang_stats)

        aux['stats'] = aux2
        return self.response.out.write(template.render( "templates/stats.html" , aux ))


def main():
    application = webapp.WSGIApplication([('/.*', Statistics)], debug=True)
    wsgiref.handlers.CGIHandler().run(application)
