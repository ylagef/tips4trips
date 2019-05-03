import webapp2
from google.appengine.api import users

from models.collaboration import Collaboration
from models.trip import Trip


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
            collaboration.put()

            self.redirect("/trips/browse?message=e71c6824d014ee17a9dfc77cae0928af")


app = webapp2.WSGIApplication([('/trips/collaborate', TripCollaborate), ], debug=True)
