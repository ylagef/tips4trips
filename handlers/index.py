import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

from models.appinfo import AppInfo
from models.message import Message


class WelcomePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            self.redirect("/trips/manage")
        else:
            user_email = ""
            access_link = users.create_login_url("/trips/manage")

            global message_type
            message_code = self.request.get("message")

            if message_code:
                if message_code.__contains__("e"):
                    message_type = "error"
                else:
                    message_type = "success"

            message = Message.message[message_code]

            template_values = {
                "info": AppInfo,
                "user_email": user_email,
                "access_link": access_link,
                "section": "none",
                "message_type": message_type,
                "message": message
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("views/index.html", **template_values))


app = webapp2.WSGIApplication([('/', WelcomePage), ], debug=True)
