#
# <( 'v' )> Work in progress! <( 'v' )>
#
# Helpful documentation:
#
# Datastore and querying:
# https://developers.google.com/appengine/docs/python/ndb/
# https://developers.google.com/appengine/docs/python/ndb/entities
# https://developers.google.com/appengine/docs/python/ndb/queries
# 
#
# Default Google Cloud Storage bucket:
# -----> A note about the library: I've gotta host it in gifhov/cloudstorage (took forever to figure this out)
# https://developers.google.com/appengine/docs/python/googlecloudstorageclient/
# https://developers.google.com/appengine/docs/python/googlecloudstorageclient/activate#Using_the_default_Gcs_bucket
#
# Working with images (resizing, etc.):
# https://developers.google.com/appengine/docs/python/images/
#
#
# Some session wizardy:
# http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html
#

import config
import views
import datastore_defs

import os
from uuid import uuid4
import urllib # This library can be used to append strings to the URL - pretty nifty

from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import memcache
from google.appengine.api import app_identity

import jinja2

import webapp2



#
# Run the application
#

application = webapp2.WSGIApplication([

	('/', views.Home),
	('/other', views.Other),
	('/register', views.Register),
	('/login', views.Login),
	('/logout', views.Logout),
	('/upload', views.Upload), 
	webapp2.Route(r'/display/<param>', handler=views.Display), # More info about routing in webapp2: http://webapp-improved.appspot.com/guide/routing.html
	webapp2.Route(r'/serve/<param>', handler=views.Serve)

], debug=True)