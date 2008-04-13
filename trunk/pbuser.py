from google.appengine.api import users

class Pbuser(object):

    def __init__(self, paste):
        self.paste = paste
        self.google_user = users.get_current_user()
        if self.google_user:
            self.nick = self.google_user.nickname()
        else:
            self.nick = "anonymous"

    def get_login_url(self):
        if self.google_user:
            return users.create_logout_url('/')
        else:
            return users.create_login_url('/')

    def logged_in(self):
        return self.google_user


    def nickname(self):
        return self.nick
