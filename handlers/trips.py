import datetime

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

from models.appinfo import AppInfo
from models.collaboration import Collaboration
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

        start = self.request.get("start")
        end = self.request.get("end")

        if place == "":
            self.redirect('/trips/add?message=edc5552973b5eea2cbc6d76s1e6fs025b')
        elif start == "" or end == "":
            self.redirect('/trips/add?message=e71c6825d054ee15a9d5c77cae0428af3')
        else:
            start = datetime.datetime.strptime(start, '%Y-%m-%d')
            end = datetime.datetime.strptime(end, '%Y-%m-%d')

            user = users.get_current_user()
            user_email = user.email()

            trip = Trip(start=start, end=end, place=place, owner=user_email)

            if trip.put():
                self.redirect('/trips/manage?message=s7870eca52ddbc23d27daacc15505718a')
            else:
                self.redirect('/trips/add?message=e71b6b22d0ad2es5s945t76cve6v29af3')


class TripsBrowse(webapp2.RequestHandler):
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


class TripCollaborate(webapp2.RequestHandler):

    def post(self):
        new_amount = self.request.get("amount")

        if new_amount == "":
            self.redirect("/trips/browse?message=ed0a1033d7809c256156d8bf0eb4673de")
        elif not new_amount.isdigit():
            self.redirect("/trips/browse?message=e4fcba5c5c609b4800a1fa6513ba42bd8")
        else:
            new_amount = int(new_amount)
            # Update wanted trip
            trip = Trip.get_by_id(int(self.request.get("trip_key")))
            past_amount = trip.collectedAmount
            trip.collectedAmount = past_amount + new_amount
            trip.put()

            collaboration = Collaboration(trip_key=int(self.request.get("trip_key")), amount=new_amount,
                                          user=users.get_current_user().email())

            if collaboration.put():
                self.redirect("/trips/browse?message=se71c6824d014ee17a9dfc77cae0928af")
            else:
                self.redirect("/trips/browse?message=e61b6b2d40ad234d5svd1f26v6d7y9a53")


class TripDelete(webapp2.RequestHandler):

    def post(self):
        trip = Trip.get_by_id(int(self.request.get("trip_key")))

        if users.get_current_user().email() != trip.owner:
            self.redirect("/trips/manage?message=e71c6822d05dees5s9a5t76c6e6429af3")
        else:
            # Get related collaborations
            collaborations = list(Collaboration.query(Collaboration.trip_key == int(self.request.get("trip_key"))))

            # Delete collaborations
            for c in collaborations:
                c.delete()
                ndb.Key(Collaboration, int(c.key.id())).delete()

            # Delete wanted trip
            if ndb.Key(Trip, int(self.request.get("trip_key"))).delete():
                self.redirect("/trips/manage?message=e55b6b2240ad2e55s9453t765v6v29a53")
            else:
                self.redirect("/trips/manage?message=sdc5552978b5eea6cbc607611e7f4025b")


class TripsManager(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        user_email = user.email()

        message_type = ""
        message = ""
        message_code = self.request.get("message")

        if message_code and Message.message.__contains__(message_code):
            message = Message.message[message_code]

            if message_code.startswith("e"):
                message_type = "error"
            else:
                message_type = "success"

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


app = webapp2.WSGIApplication([
    ('/trips/add', TripAdd),
    ('/trips/browse', TripsBrowse),
    ('/trips/collaborate', TripCollaborate),
    ('/trips/delete', TripDelete),
    ('/trips/manage', TripsManager)
], debug=True)
