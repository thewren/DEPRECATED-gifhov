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
# Functions
#

def generate_id():
	'''Generate a unique alphanumeric 12 digit id using uuid.uuid4().  Before comitting the returned
	value of this funtion, you should verify the returned value does not already exist in your database . . .
	. . . you never know!'''

	a, b, c, d, userid = str(uuid4()).split('-')

	return userid

#
# Datastore Definitions
#

class User(ndb.Model):
	"""Models a user of Gifhov in the datastore"""

	userid = ndb.StringProperty()
	useremail = ndb.StringProperty()
	username = ndb.StringProperty()
	password = ndb.StringProperty()
	usergroup = ndb.StringProperty()
	joindate = ndb.DateTimeProperty(auto_now_add=True)

class Gifhov(ndb.Model):
	'''Models a Gifhov in the datastore'''
	uploadid = ndb.StringProperty()
	userid = ndb.StringProperty()
	title = ndb.StringProperty()
	gifblobkey = ndb.BlobKeyProperty()
	audioblobkey = ndb.BlobKeyProperty()
	uploaddate = ndb.DateTimeProperty(auto_now_add=True)
	tags = ndb.StringProperty()


#
# Views
#
class Home(webapp2.RequestHandler):

	def get(self):
		success = None

		# Get an upload URL to upload files to the blob store
		# Uploads are handled by the Upload class, a subclass of blobstore_handlers.BlobstoreUploadHandler
		upload_url = blobstore.create_upload_url('/upload')

		# Query the Gifhov entity for the most recently uploaded gifhov!
		qry = Gifhov.query().order(-Gifhov.uploaddate).fetch(1)[0]
		#gqry = ndb.gql('SELECT uploadid FROM Gifhov ORDER BY uploaddate DESC').fetch(1)[0]


		template = config.JINJA_ENVIRONMENT.get_template('templates/home.html')
		return self.response.write(template.render(
													success = True,
													upload_url = upload_url,
													gif = qry.gifblobkey,
													audio = qry.audioblobkey
													))



class Upload(blobstore_handlers.BlobstoreUploadHandler):

	def post(self):
		
		# Get the files from the form
		giffile = self.get_uploads('gif')
		gifblobinfo = giffile[0]

		audiofile = self.get_uploads('audio')
		audioblobinfo = audiofile[0]

		# Write the Gifhov to the datastore
		gifhov = Gifhov()

		gifhov.uploadid = generate_id()
		gifhov.userid = 'REPLACE ME'
		gifhov.title = 'REPLACE ME'
		gifhov.gifblobkey = gifblobinfo.key()
		gifhov.audioblobkey = audioblobinfo.key()
		# gifhov.uploaddate is automatically generated when a new entity is created, so we don't have to set it
		gifhov.tags = 'REPLACE ME'

		gifhov.put()


		# Redirect to the homepage after creating the Gifhov
		self.redirect('/')
		



class Serve(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, param):
		blob_info = blobstore.BlobInfo.get(param)
		self.send_blob(blob_info)




class Other(webapp2.RequestHandler):
	'''Print session information in the terminal'''
	def get(self):

		session = {
			'Logged in: ':memcache.get('logged_in'),
			'User ID: ':memcache.get('user_id')

		}

		if session is not None:
			print session
		else:
			print 'No session data'

		template=config.JINJA_ENVIRONMENT.get_template('templates/other.html')
		return self.response.write(template.render())




class Display(webapp2.RequestHandler):

	def get(self, param):
		template = config.JINJA_ENVIRONMENT.get_template('templates/other.html')
		return self.response.write(template.render(message = 'URL appended with: %s' % param))



class Register(webapp2.RequestHandler):

	def get(self):
		success = None
		error = None

		template = config.JINJA_ENVIRONMENT.get_template('templates/register.html')
		return self.response.write(template.render(success = success, error = error))		



	def post(self):

		# Declare the entity type
		user = User()

		success = None
		error = None

		# Retrieve the user-entered form data
		email = self.request.get('email')
		username = self.request.get('username')
		password = self.request.get('password')

		# Verify that the email contains essentials; pass an error if it doesn't
		if '@' and '.' not in email:
			error = "Your email address must contain '@' and '.'"
			template = config.JINJA_ENVIRONMENT.get_template('templates/register.html')
			return self.response.write(template.render(success = success, error = error))

		# Query the datastore for Users who already have the entered email
		qry = User.query(User.useremail == email).fetch(1)

		# Check to see if an account with the entered email already exists; pass an error if one does
		try:
			if email == qry[0].useremail:
				error = 'An account with that email address already exists'
				template = config.JINJA_ENVIRONMENT.get_template('templates/register.html')
				return self.response.write(template.render(success = success, error = error))

		# If the no row is returned, an IndexError is thrown, but it indicates that there is no match, so we should write the new user to the datastore
		except IndexError:

			# Write the new user to the datastore
			user.userid = generate_id()
			user.useremail = email
			user.username = username
			user.password = password
			user.usergroup = 'general'

			user_key = user.put()

			success = True

		template = config.JINJA_ENVIRONMENT.get_template('templates/register.html')
		return self.response.write(template.render(success = success, error = error))



class Login(webapp2.RequestHandler):

	def get(self):
		template = config.JINJA_ENVIRONMENT.get_template('templates/login.html')
		return self.response.write(template.render())

	def post(self):

		# Declare the entity type
		user = User()
		error = None

		email = self.request.get('email')
		password = self.request.get('password')

		# Verify that the entered account credentials match credentials in the datastore
		try:
			# Query the User entity to see if there is a match based on the entered email
			qry = User.query(User.useremail == email).fetch(1)

			# Verify the email is correct, throw an error if it isn't
			if email != qry[0].useremail:
				error = 'Incorrect email address'

			# Verify the password is correct; throw an error if it isn't
			elif password != qry[0].password:
				error = 'Incorrect password'

			# If the credentials are correct, log the user in,make a note in their secure cookie session, and redirect to home.html
			else:
				# Add a 'logged_in' key to the memcache; set the value to True; expire it in 1 hour
				memcache.add(key='logged_in', value=True, time=3600)

				# Add the user id to the memcahce, expire it in 1 hour
				memcache.add(key='user_id', value=qry[0].userid, time=3600)

				template = config.JINJA_ENVIRONMENT.get_template('templates/home.html')
				return self.response.write(template.render())

		except IndexError:
			error = 'An account with the specified credentials does not exist'

		template = config.JINJA_ENVIRONMENT.get_template('templates/login.html')
		return self.response.write(template.render(error = error))




class Logout(webapp2.RequestHandler):

	def get(self):

		if memcache.get('logged_in') == True:
			memcache.flush_all()

		template = config.JINJA_ENVIRONMENT.get_template('templates/home.html')
		return self.response.write(template.render())