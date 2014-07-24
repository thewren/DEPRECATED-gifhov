#
# Datastore
# Helpful documentation: https://developers.google.com/datastore/docs/concepts/entities#Datastore_Creating_an_entity
#


from google.appengine.ext import ndb


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