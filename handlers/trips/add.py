import datetime

import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

from models.appinfo import AppInfo
from models.message import Message
from models.trip import Trip


class TripAdd(webapp2.RequestHandler):
    def get(self):
        message_type = ""
        message = ""
        message_code = self.request.get("message")

        if message_code and Message.message.__contains__(message_code):
            message = Message.message[message_code]

            if message_code.startswith("e"):
                message_type = "error"
            else:
                message_type = "success"

        user = users.get_current_user()
        user_email = user.email()

        access_link = users.create_logout_url("/")

        template_values = {
            "info": AppInfo,
            "user_email": user_email,
            "access_link": access_link,
            "section": "newTrip",
            "message_type": message_type,
            "message": message
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("views/trips/add.html", **template_values))

    def post(self):
        place = self.request.get("place")
        start = datetime.datetime.strptime(self.request.get("start"), '%Y-%m-%d')
        end = datetime.datetime.strptime(self.request.get("end"), '%Y-%m-%d')

        if place == "":
            self.redirect('/trips/add?message=edc5552973b5eea2cbc6d76s1e6fs025b')
        elif start == "" and end == "":
            self.redirect('/trips/add?message=e71c6825d054ee15a9d5c77cae0428af3')
        else:
            user = users.get_current_user()
            user_email = user.email()

            trip = Trip(start=start, end=end, place=place, owner=user_email)
            trip.put()

            self.redirect('/trips/manage?message=s7870eca52ddbc23d27daacc15505718a')


app = webapp2.WSGIApplication([('/trips/add', TripAdd), ], debug=True)
