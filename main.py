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
        email = users.get_current_user()
        #Assign these to something so the python runs
        nickname = None
        logout_url = None
        login_url = None

        if email:
            nickname = email.nickname()
            logout_url = users.create_logout_url('/')
        else:
            login_url = users.create_login_url('/')
        template_vars = {
            "email": email,
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
class DashboardHandler(webapp2.RequestHandler):
    def get(self):
        email = users.get_current_user()
        if not email:
            self.redirect("/home")
        else:
            logout_url = users.create_logout_url('/')
        template_vars = {
            "logout_url": logout_url,
        }
        template = jinja_current_dir.get_template("/templates/dashboard.html")
        self.response.write(template.render(template_vars))
class User(ndb.Model):
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    bio = ndb.TextProperty()
    location = ndb.StringProperty()
class EditProfileHandler(webapp2.RequestHandler):
    def get(self):
        email = users.get_current_user()
        if not email:
            self.redirect("/home")
        else:
            logout_url = users.create_logout_url('/')
        template_vars = {
            "logout_url": logout_url,
        }
        template = jinja_current_dir.get_template("/templates/edit_profile.html")
        self.response.write(template.render(template_vars))
    def post(self):
        email = users.get_current_user()
        username = self.request.get('username')
        bio = self.request.get('bio')
        location = self.request.get('location')

        current_user = User(email = email.email(), username = username, bio = bio, location = location)
        current_user.put()

        self.redirect("/view_profile")

class ViewProfileHandler(webapp2.RequestHandler):
    def get(self):
        email = users.get_current_user()
        if not email:
            self.redirect("/home")
        else:
            current_user = User.query(User.email == email.email()).fetch()
            if len(current_user) == 0:
                self.redirect("/edit_profile")
            else:
                biography = current_user[0].bio
                template_vars = {
                    "username": current_user[0].username,
                    "biography": biography, 
                }
                template = jinja_current_dir.get_template('/templates/view_profile.html')
                self.response.write(template.render(template_vars))
class PlacesHandler(webapp2.RequestHandler):
    def get(self):
        email = users.get_current_user()
        if not email:
            self.redirect("/home")
        else:
            logout_url = users.create_logout_url('/')
        template_vars = {
            "logout_url": logout_url,
        }
        template = jinja_current_dir.get_template("/templates/places.html")
        self.response.write(template.render(template_vars))
class PeopleHandler(webapp2.RequestHandler):
    def get(self):
        email = users.get_current_user()
        if not email:
            self.redirect("/home")
        else:
            logout_url = users.create_logout_url('/')
        template_vars = {
            "logout_url": logout_url,
        }
        template = jinja_current_dir.get_template("/templates/people.html")
        self.response.write(template.render(template_vars))
app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/home', MainHandler), ('/about', AboutHandler),
    ('/dashboard', DashboardHandler), ('/view_profile', ViewProfileHandler),
    ('/edit_profile', EditProfileHandler), ('/places',PlacesHandler),
    ('/people',PeopleHandler),
], debug=True)
