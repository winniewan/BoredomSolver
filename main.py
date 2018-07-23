import webapp2
import os
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users


jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        #Assign these to something so the python runs
        nickname = None
        logout_url = None
        login_url = None

        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
        else:
            login_url = users.create_login_url('/')
        template_vars = {
            "user": user,
            "nickname": nickname,
            "logout_url": logout_url,
            "login_url": login_url,

        }
        template = jinja_current_dir.get_template("/templates/home.html")
        self.response.write(template.render(template_vars))
class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("/templates/about.html")
        self.response.write(template.render())
app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/home', MainHandler), ('/about', AboutHandler),
], debug=True)
