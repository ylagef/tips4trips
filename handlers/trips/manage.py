import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

import models.user as user_mgt
from models.appinfo import AppInfo
from models.trip import Trip
from models.user import User


class TripsManager(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        user_info = user_mgt.retrieve(user)

        if user and user_info:
            access_link = users.create_logout_url("/")

            trips = Trip.query(Trip.owner == user_info.email).order(Trip.start)

            print("before - " + user_info.email)
            print(trips)
            print("after")

            template_values = {
                "info": AppInfo,
                "user_info": user_info,
                "access_link": access_link,
                "Level": User.Level,
                "trips": trips
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("views/trips/manage.html", **template_values))
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([('/trips/manage', TripsManager), ], debug=True)
