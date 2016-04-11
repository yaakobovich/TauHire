﻿#!/usr/bin/env python
import cgi
import urllib
import datetime
import logging

from google.appengine.api import users
from google.appengine.ext import ndb
from oauth2client.client import flow_from_clientsecrets
from oauth2client import client, crypt

import webapp2

from db import *
from messages import *


#end of DB class definitions
#
#
#classes for actions:


class CompanyHandler(webapp2.RequestHandler):
    def get(self):
        f = open("companyQueryFormPage\index.html") 
	#self.response.charset="unicode"
	self.response.write(f.read())
	f.close()               

class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
			self.response.write('Hello, ' + user.nickname())
			# self.response.write('<div><a href="/chooseEmployOrStudentPage/index.html">login</a></div>')				
			self.response.write('<html> <script src="https://apis.google.com/js/platform.js" async defer></script>')
			self.response.write('<meta name="google-signin-client_id" content="412529039560-acrgsqrqqit5no5d8am0jajjtei5jqua.apps.googleusercontent.com">')
			self.response.write('<div class="g-signin2" data-onsuccess="onSignIn"></div>')
			self.response.write("""<script> function onSignIn(googleUser){
				var id_token = googleUser.getAuthResponse().id_token;
				var profile = googleUser.getBasicProfile();
				console.log('idToken: ' + id_token);
				console.log('Name: ' + profile.getName());
				console.log('Image URL: ' + profile.getImageUrl());
				console.log('Email: ' + profile.getEmail()); 
				var xhr = new XMLHttpRequest();
				xhr.open('POST', '/tokenSignIn');
				xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
				xhr.onload = function() {
				console.log('Signed in as: ' + xhr.responseText);
				window.location="chooseEmployOrStudentPage/index.html";
				};
				//xhr.send('idtoken=' + id_token) ;
				xhr.send('<br><br>email=' + profile.getEmail())}

				</script>""")
			self.response.write('<a href="#" onclick="signOut();">Sign out</a>')
			self.response.write("""<script> function signOut() {
				var auth2 = gapi.auth2.getAuthInstance();
				auth2.signOut().then(function () {
					console.log('User signed out.');
						});
					}
				</script>""")

			#self.response.write('<div><a href="/chooseEmployOrStudentPage/index.html">login</a></div>')	
		else: 
			self.redirect(users.create_login_url(self.request.uri))

class tokenSignIn(webapp2.RequestHandler):
	def post(self):
		logging.info(self.request)
		#self.response.write("<html>")
		#self.response.write(self.request)
		token=self.request.get('idtoken')
		# (Receive token by HTTPS POST)
		
		try:
			idinfo = client.verify_id_token(token, "412529039560-acrgsqrqqit5no5d8am0jajjtei5jqua.apps.googleusercontent.com")
			# If multiple clients access the backend server:
			# if idinfo['aud'] not in [ANDROID_CLIENT_ID, IOS_CLIENT_ID, WEB_CLIENT_ID]:
			# 	raise crypt.AppIdentityError("Unrecognized client.")
			if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
				raise crypt.AppIdentityError("Wrong issuer.")
			# if idinfo['hd'] != APPS_DOMAIN_NAME:
			# 	raise crypt.AppIdentityError("Wrong hosted domain.")
		except crypt.AppIdentityError:
			# Invalid token
			pass
		
		#st= Student(id=users.get_current_user().user_id())
		userid = idinfo['sub']
		user_query = Student.query(Student.id==userid).get()
		#entity = Student.get_by_id(int(userid))
		logging.info(user_query)
		if (user_query == None):
			s = []
		
			st= Student(student_courses=s,id=userid, name="demo", email = self.request.get('email'), city="demo",avg=40)
			st.put()
			logging.info('token info')
			self.response.write('<html><br><br>userId: ' + userid)


class LoginHandler(webapp2.RequestHandler):
    def get(self):
    	# flow = flow_from_clientsecrets('/client_secrets.json',
     #                           scope='email',
     #                           redirect_uri='www.google.co.il')
    	# auth_uri = flow.step1_get_authorize_url()
    	# # Redirect the user to auth_uri on your platform.
    	# self.response.write('<a href="' + auth_uri + '">Login With Google</a>')
		f = open("chooseEmployOrStudentPage/index.html") 
		self.response.write(f.read())
		f.close() 

class MainHandler(webapp2.RequestHandler):
    def get(self):
        f = open("studentInputPage/index.html") 
	#self.response.charset="unicode"
	self.response.write(f.read())
	f.close()        


class ResultsPage(webapp2.RequestHandler):
	def get(self):
		f = open("companyQueryResultsPage/index.html")		
		self.response.write(f.read())
		f.close()

class FirstPage(webapp2.RequestHandler):
	def get(self):
		self.response.write ("""<html><script>
			window.location="chooseEmployOrStudentPage/index.html";
			</script></html>""")

app = webapp2.WSGIApplication([
	#('/MainPage', MainPage),
	('/', MainPage),
	('/dbDelete', dbDelete),
	('/dbBuild', dbBuild),
	('/studentInputPage/index.html', MainHandler),
	('/tokenSignIn', tokenSignIn),
	('/chooseEmployOrStudentPage/index.html', LoginHandler),
	#('/', FirstPage),
	('/dbHandler', dbHandler),
	('/companyQueryFormPage/index.html', CompanyHandler),
	('/companyQueryResultsPage' , minGradeQuery),
	('/StudentOffersPage', MessageHandler),
	('/messageSend', MessageSend),
	('/messageReply', MessageReply)	
	], debug=True)


	
