from google.appengine.ext.webapp import template
from google.appengine.ext import db

from paste import Paste

class Site(object):

    """Currently handles the what to show on the front end"""

    def __init__(self, ctx, user):
        self.ctx = ctx
        self.user = user

    def get_content(self, **kwds):
        #for debugging:
        self.write = self.ctx.response.out.write

        tvars = {"user":self.user}
        path_parts = self.ctx.request.path.split('/')
        uid = None

        try:
            uid = kwds["uid"]
        except KeyError:
            tvars["url"] = None

        if len(path_parts) > 2 and path_parts[1] == "p":
            uid = path_parts[2]

        if uid:
            paste = Paste()
            #XXX: need to check for errors here
            data = paste.gql("WHERE uid = :1", uid)[0]
            if data:
                tvars = self.get_display_paste(data, tvars, uid)
            else:
                tvars = self.get_empty_display(tvars)
        else:
            tvars = self.get_empty_display(tvars)
            try:
                tvars["issues"] = kwds["issues"]
                t = kwds["vars"] #t for temporary
                tvars = self.set_paste_data(tvars,t["title"],t["code"],t["comment"])
            except KeyError:
                tvars["issues"] = None

        return template.render("templates/index.html", tvars)

    def clean_whitespace(self, raw):
        spaces_per_tab = 4
        raw = "".join([ (("&nbsp;" * spaces_per_tab) if (i == "\t") else i ) for i in raw])
        return "".join([ ("&nbsp;" if (i == " ") else i) for i in raw ])



    def get_display_paste(self, data, tvars, uid):
        import xml.sax.saxutils as saxutils
        clean_code = self.clean_whitespace(saxutils.escape(data.code))
        tvars = self.set_paste_data(tvars, data.title, data.code, data.comment)
        tvars["isPaste"] = True
        tvars["url"] = self.ctx.request.application_url + "/p/" + uid
        tvars["codeList"] =  clean_code.split("\n")
        return tvars

    def set_paste_data(self, tvars, title, code, comment):
        tvars["title"] = title
        tvars["comment"] = comment
        tvars["codeRaw"] = code
        return tvars

    def get_empty_display(self, tvars):
        tvars["isPaste"] = False 
        tvars["title"] = ""
        tvars["comment"] = ""
        tvars["codeRaw"] = ""
        return tvars
