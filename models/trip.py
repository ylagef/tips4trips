#!/usr/bin/env python

from google.appengine.ext import ndb


class Trip(ndb.Model):
    start = ndb.DateProperty()
    end = ndb.DateProperty()
    place = ndb.TextProperty()
    owner = ndb.TextProperty(indexed=True)
    collectedAmount = ndb.FloatProperty(default=0.0)
