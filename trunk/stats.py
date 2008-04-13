from google.appengine.ext import db

class Stats(db.Model):

    type = db.StringProperty()
    number = db.IntegerProperty()
    
