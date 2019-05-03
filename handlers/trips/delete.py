import webapp2
from google.appengine.ext import ndb

from models.collaboration import Collaboration
from models.trip import Trip


class TripDelete(webapp2.RequestHandler):

    def post(self):
        # Get related collaborations
        collaborations = list(Collaboration.query(Collaboration.trip_key == int(self.request.get("trip_key"))))

        # Delete collaborations
        for c in collaborations:
            ndb.Key(Collaboration, int(c.key.id())).delete()

        # Delete wanted trip
        ndb.Key(Trip, int(self.request.get("trip_key"))).delete()

        self.redirect("/trips/manage?message=dc5552978b5eea6cbc607611e7f4025b")


app = webapp2.WSGIApplication([('/trips/delete', TripDelete), ], debug=True)
