#!/usr/bin/env python

from google.appengine.ext import ndb


class Collaboration(ndb.Model):
    trip_key = ndb.IntegerProperty(indexed=True)
    amount = ndb.FloatProperty(default=0.0)
    date = ndb.DateProperty(auto_now_add=True, indexed=True)
    user = ndb.TextProperty()
