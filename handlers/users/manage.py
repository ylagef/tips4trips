# infra-esei-tickets (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

import models.user as user_mgt
from models.appinfo import AppInfo
from models.user import User


class UsersManager(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        user_info = user_mgt.retrieve(user)

        if user and user_info:
            user_admin_set = User.query(User.level == User.Level.Admin).order(-User.added)
            user_staff_set = User.query(User.level != User.Level.Admin).order(User.level).order(-User.added)
            user_set = list(user_admin_set) + list(user_staff_set)
            access_link = users.create_logout_url("/")

            if not (user_info.is_admin()):
                self.redirect("/error?msg=User " + user_info.nick + " not allowed to manage users")
                return

            template_values = {
                "info": AppInfo,
                "user_info": user_info,
                "access_link": access_link,
                "users": user_set,
                "Level": User.Level,
                "section": "manage"
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("users.html", **template_values))
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([('/manage_users', UsersManager), ], debug=True)
