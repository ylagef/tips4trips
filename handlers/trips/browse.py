import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

from models.appinfo import AppInfo
from models.message import Message
from models.trip import Trip


class TripsBrowser(webapp2.RequestHandler):
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

        trips = list(Trip.query().order(Trip.start))

        template_values = {
            "info": AppInfo,
            "user_email": user_email,
            "access_link": access_link,
            "trips": trips,
            "section": "browse",
            "message_type": message_type,
            "message": message
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("views/trips/browse.html", **template_values))


app = webapp2.WSGIApplication([('/trips/browse', TripsBrowser), ], debug=True)
