import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

import models.user as user_mgt
from models.appinfo import AppInfo


class WelcomePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        user_info = user_mgt.retrieve(user)

        if user and user_info:
            self.redirect("/trips/manage")
            return
        else:
            user_info = user_mgt.create_empty_user()
            user_info.nick = "Login"
            access_link = users.create_login_url("/trips/manage")

        template_values = {
            "info": AppInfo,
            "user_info": user_info,
            "access_link": access_link
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("views/index.html", **template_values))


app = webapp2.WSGIApplication([('/', WelcomePage), ], debug=True)
