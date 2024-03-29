from google.appengine.ext.webapp import template

from syntax import Syntax

class Site(object):
    """Currently handles the what to show on the front end"""


    def __init__(self, ctx, values):
        self.ctx = ctx
        self.values = values
        self.user = self.ctx.curr_user.nickname()


    def get_content(self, **kwds):
        """Returns the content for the page"""

        #for debugging:
        #self.write = self.ctx.response.out.write

        tvars = {"user":self.user, "user_short":self.user.split("@")[0]}
        path_parts = self.ctx.request.path.split('/')
        uid = None

        if "uid" in kwds:
            uid = kwds["uid"]
        else:
            tvars["url"] = None
            if len(path_parts) > 2 and path_parts[1] == "p":
                uid = path_parts[2]

        if uid:
            try:
                data = self.ctx.db.paste.gql("WHERE uid = :1", uid)[0]
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


        query = self.ctx.db.paste.all()
        try:
            query.filter('name =', self.ctx.curr_user.nickname()).order("-date")
            tvars["user_paste_count"] = query.count()
            tvars["user_pastes"] = query.fetch(10)
        except IndexError: 
            tvars["user_paste_count"] = 0
            tvars["user_pastes"] = None
        tvars["types"] = Syntax.get_type_list()
        tvars["types"].sort()
        tvars["application_url"] = self.ctx.request.application_url 
        tvars.update(self.values)
        return template.render("templates/index.html", tvars)


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
