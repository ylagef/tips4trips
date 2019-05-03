import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

from models.appinfo import AppInfo
from models.collaboration import Collaboration
from models.message import Message
from models.trip import Trip


class TripsManager(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        user_email = user.email()

        message_type = ""
        message = ""
        message_code = self.request.get("message")

        if message_code:
            if message_code.__contains__("e"):
                message_type = "error"
            else:
                message_type = "success"
            message = Message.message[message_code]

        access_link = users.create_logout_url("/")

        trips = list(Trip.query(Trip.owner == user_email).order(Trip.start))

        all_collaborations = dict()
        for t in trips:
            trip_collaborations = list(
                Collaboration.query(Collaboration.trip_key == t.key.id()).order(Collaboration.date))
            all_collaborations[t.key.id()] = trip_collaborations

        template_values = {
            "info": AppInfo,
            "user_email": user_email,
            "access_link": access_link,
            "trips": trips,
            "section": "manage",
            "collaborations": all_collaborations,
            "message_type": message_type,
            "message": message
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("views/trips/manage.html", **template_values))


app = webapp2.WSGIApplication([('/trips/manage', TripsManager), ], debug=True)
