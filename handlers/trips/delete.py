import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

import models.user as user_mgt
from models.appinfo import AppInfo
from models.trip import Trip
from models.user import User


class TripDelete(webapp2.RequestHandler):

    def get(self):
        trip_key = self.request.get("trip_key")

        user = users.get_current_user()
        user_info = user_mgt.retrieve(user)

        if user and user_info:
            access_link = users.create_logout_url("/")

            # Delete wanted trip
            ndb.Key(Trip, int(self.request.get("trip_key"))).delete()

            # Retrieve trips after deletion
            trips = Trip.query(Trip.owner == user_info.email).order(Trip.start)

            template_values = {
                "info": AppInfo,
                "user_info": user_info,
                "access_link": access_link,
                "Level": User.Level,
                "trips": trips,
                "section": "manage"
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("views/trips/manage.html", **template_values))


app = webapp2.WSGIApplication([('/trips/delete', TripDelete), ], debug=True)
