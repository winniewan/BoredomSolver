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
class DashboardHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("/templates/dashboard.html")
        self.response.write(template.render())
class Post(ndb.Model):
    bio = ndb.TextProperty()
class User(ndb.Model):
    username = ndb.StringProperty()
    bio = ndb.KeyProperty(kind = Post, repeated = True)
class EditProfileHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("/templates/edit_profile.html")
        self.response.write(template.render())
    def post(self):
        username = self.request.get('username')
        bio = self.request.get('bio')

        bio = Post(bio = bio)
        bio.put()

        check_user = User.query(User.username == username).fetch()
        user = User(username = username , bio = [bio.key])
        if check_user:
            check_user[0].bio.append(bio.key)
        else:
            user.put()

        bios = []
        for bio_key in user.bio:
            bios.append(bio_key.get().bio)

        template_vars = {
            'username' : username ,
            'bios' : bios
        }
        template = jinja_current_dir.get_template('/templates/view_profile.html')
        self.response.write(template.render(template_vars))

class ViewProfileHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        check_users = User.query(User.username == username).fetch()
        if check_users:
            user = check_users[0]
        else:
            self.redirect("/edit_profile")
        bios = []
        for bio_key in user.bio:
            bios.append(bio_key.get())

        template_vars = {
            'username' : username ,
            'bios' : bios
        }
        template = jinja_current_dir.get_template('/templates/view_profile.html')
        self.response.write(template.render(template_vars))
class PlacesHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("/templates/places.html")
        self.response.write(template.render())
class PeopleHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("/templates/people.html")
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/home', MainHandler), ('/about', AboutHandler),
    ('/dashboard', DashboardHandler), ('/view_profile', ViewProfileHandler),
    ('/edit_profile', EditProfileHandler), ('/places',PlacesHandler),
    ('/people',PeopleHandler),
], debug=True)
