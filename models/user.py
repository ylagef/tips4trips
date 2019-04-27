#!/usr/bin/env python
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>


from google.appengine.api import users
from google.appengine.ext import ndb

from models.enum import Enum


class User(ndb.Model):
    Level = Enum([
        "Admin",  # Can do anything
        "Staff",  # Can create tickets, make comments and close them.
        "Client"  # Can just read and make comments.
    ], start=400, default=2)

    added = ndb.DateProperty(auto_now_add=True, indexed=True)
    email = ndb.TextProperty(indexed=True)
    nick = ndb.TextProperty(indexed=True)
    level = ndb.IntegerProperty()

    def is_admin(self):
        return self.level == User.Level.Admin or users.is_current_user_admin()

    def is_client(self):
        return self.level == User.Level.Client

    def __str__(self):
        return User.Level.values[self.level] + " (" + self.email + ")"

    def __unicode__(self):
        return User.Level.values[self.level] + ": " + self.nick + " (" + self.email + ")"


def create(user, level):
    """Creates a new user object, from GAE's user object.

        :param user: The GAE user object.
        :param level: The desired level.
        :return: A new User object."""
    toret = User()

    toret.email = user.email()
    toret.nick = user.nickname()
    toret.level = level

    return toret


def create_empty_user():
    """Used when there the user is not important."""
    return User(email="", nick="", level=User.Level.Client)


@ndb.transactional
def update(user):
    """Updates a user.

        :param user: The user to update.
        :return: The key of the record.
    """
    return user.put()


def retrieve(user):
    """Reads the user info from the database.

    :param user: The GAE user object.
    :return: The User retrieved, or a client created appropriately if not found.
    """
    toret = None

    if user:
        user_email = user.email()
        found_users = User.query(User.email == user_email).order(-User.added)

        if (found_users.count() == 0
                and users.is_current_user_admin()):
            toret = create(user, User.Level.Admin)
            update(toret)
        else:
            if found_users.count() == 0:
                toret = create(user, User.Level.Client)
            else:
                toret = found_users.iter().next()
                toret.user = user

    return toret
