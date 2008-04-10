from google.appengine.ext import db
from google.appengine.api import users

class Paste(db.Model):

    uid = db.StringProperty()
    name = db.StringProperty()
    code = db.TextProperty()
    type = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    title = db.StringProperty()
    comment = db.TextProperty()
    views = db.IntegerProperty()
    tags = db.StringProperty()


