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

        if message_code:
            if message_code.__contains__("e"):
                message_type = "error"
            else:
                message_type = "success"
            message = Message.message[message_code]

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
        user = users.get_current_user()
        user_email = user.email()

        place = self.request.get("place")
        start = datetime.datetime.strptime(self.request.get("start"), '%Y-%m-%d')
        end = datetime.datetime.strptime(self.request.get("end"), '%Y-%m-%d')

        trip = Trip(start=start, end=end, place=place, owner=user_email)
        trip.put()

        self.redirect('/trips/manage?message=7870eca52ddbc23d27daacc15505718a')


app = webapp2.WSGIApplication([('/trips/add', TripAdd), ], debug=True)
