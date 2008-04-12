from google.appengine.ext.webapp import template
from google.appengine.ext import db

from paste import Paste
from syntax import Syntax

class Site(object):

    """Currently handles the what to show on the front end"""

    def __init__(self, ctx, values):
        self.ctx = ctx
        self.values = values
        self.user = values['user']

    def get_content(self, **kwds):
        #for debugging:

        
        self.write = self.ctx.response.out.write

        tvars = {"user":self.user}
        path_parts = self.ctx.request.path.split('/')
        uid = None

        if "uid" in kwds:
            uid = kwds["uid"]
        else:
            tvars["url"] = None

        if len(path_parts) > 2 and path_parts[1] == "p":
            uid = path_parts[2]

        if uid:
            paste = Paste()
            #XXX: need to check for errors here
            try:
                data = paste.gql("WHERE uid = :1", uid)[0]
                tvars = self.get_display_paste(data, tvars, uid)
            except IndexError: 
                tvars = self.get_empty_display(tvars)
        else:
            tvars = self.get_empty_display(tvars)
            if "issues" in kwds:
                tvars["issues"] = kwds["issues"]
                if "vars" in kwds:
                    t = kwds["vars"] #t for temporary
                tvars = self.set_paste_data(tvars,t["title"],t["code"],t["comment"])
            else:
                tvars["issues"] = None

        tvars["types"] = Syntax.get_type_list()
        tvars["types"].sort()
        tvars.update(self.values)
        return template.render("templates/index.html", tvars)

    def clean_whitespace(self, raw):
        #XXX: need to use string replace here
        spaces_per_tab = 4
        raw = "".join([ (("&nbsp;" * spaces_per_tab) if (i == "\t") else i ) for i in raw])
        return "".join([ ("&nbsp;" if (i == " ") else i) for i in raw ])

    def get_display_paste(self, data, tvars, uid):
        import xml.sax.saxutils as saxutils
        from syntax import Syntax
        tvars = self.set_paste_data(tvars, data.title, data.code, data.comment, data.type)
        tvars["isPaste"] = True
        tvars["url"] = self.ctx.request.application_url + "/p/" + uid
        tvars["codeFormatted"] = Syntax.get_highlighted_code(data.code, data.type)
        return tvars

    def set_paste_data(self, tvars, title, code, comment, type="text"):
        tvars["title"] = title
        tvars["comment"] = comment
        tvars["codeRaw"] = code
        tvars["type"] = type 
        return tvars

    def get_empty_display(self, tvars):
        tvars["isPaste"] = False 
        tvars["title"] = ""
        tvars["comment"] = ""
        tvars["codeRaw"] = ""
        tvars["codeFormatted"] = None
        tvars["type"] = "text"
        return tvars
