from google.appengine.ext.webapp import template
from google.appengine.ext import db

from paste import Paste

class Site(object):

    """Currently handles the what to show on the front end"""

    def __init__(self, ctx, user):
        self.ctx = ctx
        self.user = user

    def getContent(self, **kwds):

        tvars = {
            "user":self.user,
        }
        
        path_parts = self.ctx.request.path.split('/')

        uid = None

        try:
            uid = kwds["uid"]
        except KeyError:
            tvars["url"] = None


        if len(path_parts) > 2 and path_parts[1] == "p":
            uid = path_parts[2]

        if uid:
            tvars["isPaste"] = True
            tvars["url"] = self.ctx.request.application_url + "/p/" + uid
            paste = Paste()
            #XXX: need to check for errors here
            data = paste.gql("WHERE uid = :1", uid)[0]
            tvars["title"] = data.title
            tvars["comment"] = data.comment
            tvars["codeList"] =  data.code.split("\n")[:-1]
            tvars["codeRaw"] = data.code
        else:
            tvars["isPaste"] = False 
            tvars["title"] = ""
            tvars["comment"] = ""
            tvars["codeRaw"] = ""



        return template.render("templates/index.html", tvars)
