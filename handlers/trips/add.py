import datetime

import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

import models.user as user_mgt
from models.appinfo import AppInfo
from models.trip import Trip
from models.user import User


class TripAdd(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        user_info = user_mgt.retrieve(user)

        if user and user_info:
            access_link = users.create_logout_url("/")

            template_values = {
                "info": AppInfo,
                "user_info": user_info,
                "access_link": access_link,
                "Level": User.Level,
                "section": "newTrip"
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("views/trips/add.html", **template_values))
        else:
            self.redirect("/")
            return

    def post(self):

        print("Place" + self.request.get("place"))

        user = users.get_current_user()
        user_info = user_mgt.retrieve(user)

        place = self.request.get("place")
        start = datetime.datetime.strptime(self.request.get("start"), '%Y-%m-%d')
        end = datetime.datetime.strptime(self.request.get("end"), '%Y-%m-%d')

        if user and user_info:
            access_link = users.create_logout_url("/")

            template_values = {
                "info": AppInfo,
                "user_info": user_info,
                "access_link": access_link,
                "Level": User.Level,
            }

            trip = Trip(start=start, end=end, place=place, owner=user_info.email)
            trip.put()

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("views/trips/manage.html", **template_values))
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([('/trips/add', TripAdd), ], debug=True)
