import webapp2
import os
import jinja2
import time
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
    place = ndb.TextProperty()
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
        place = self.request.get('place')
        location = self.request.get('location')

        current_user = User.query(User.email == email.email()).fetch()

        if len(current_user) <= 0:
            current_user = User(username = username, email = email.email(), bio = bio, place = place, location = location)
        else:
            current_user = current_user[0]
            if username == "":
                username = current_user.username
            if bio == "":
                bio = current_user.bio
            if place == "":
                place = current_user.place
            if location == "":
                location = current_user.location

            current_user.username = username
            current_user.bio = bio
            current_user.place = place
            current_user.location = location

        current_user.put()
        time.sleep(0.5)
        self.redirect("/view_profile")

class ViewProfileHandler(webapp2.RequestHandler):
    def get(self):
        email = users.get_current_user()
        current_user = User.query(User.email == email.email()).fetch()

        if not email:
            self.redirect("/home")
        else:
            logout_url = users.create_logout_url('/')
            current_user = User.query(User.email == email.email()).fetch()
            diff_email = self.request.get("email")

            if len(current_user) == 0:
                self.redirect("/edit_profile")
            else:
                if not diff_email == "":
                    current_user = User.query(User.email == diff_email).fetch()
                biography = current_user[0].bio
                places = current_user[0].place
                email = current_user[0].email
                location = current_user[0].location
                template_vars = {
                    "logout_url": logout_url,
                    "username": current_user[0].username,
                    "biography": biography,
                    "places": places,
                    "email": email,
                    "location": location,
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
        all_users = User.query().fetch()
        template_vars = {
            "logout_url": logout_url,
            "users": all_users,
        }
        template = jinja_current_dir.get_template("/templates/people.html")
        self.response.write(template.render(template_vars))
app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/home', MainHandler), ('/about', AboutHandler),
    ('/dashboard', DashboardHandler), ('/view_profile', ViewProfileHandler),
    ('/edit_profile', EditProfileHandler), ('/places',PlacesHandler),
    ('/people',PeopleHandler),
], debug=True)
