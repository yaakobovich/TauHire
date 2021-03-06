import cgi
import urllib
import datetime
import time as t

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail


import webapp2
import logging

import db 

from main import *
from db import *
from methods import *


MESSAGE_PAGE_HTML = """\
<html>
  <body>
    <form action="/messageSend" method="post">
	  send to:
	  <input type="text" name="recv" ><br>
      <div><textarea name="mess" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="send message"></div>
    </form>
	<br><br>
	</div><p>messages:</p><div>
	
  </body>
</html>
"""


# classes for the message system
class threadNum(ndb.Model):
	num = ndb.IntegerProperty(indexed = False)

class Author(ndb.Model):
	identity = ndb.StringProperty(indexed=False)

class Message(ndb.Model):
	#thread = ndb.IntegerProperty(indexed = False)
	sender = ndb.StructuredProperty(Author)
	receiver = ndb.StructuredProperty(Author)
	#receiver = ndb.StringProperty(indexed=False)
	cont = ndb.StringProperty(indexed=False)
	compMail = ndb.StringProperty(indexed=True)
	compName = ndb.StringProperty(indexed=False)
	compLocation = ndb.StringProperty(indexed=False)
	jobName = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

class Conversation(ndb.Model):
	id = ndb.StringProperty(indexed = False)
	message = ndb.StructuredProperty(Message, repeated=True)
	#parameters	

class Ad(ndb.Model):
	user_id = ndb.StringProperty(indexed=True, required=True)
	sentId = ndb.StringProperty(repeated=True)
	studNum = ndb.StringProperty(indexed=True, required=False)
	message = ndb.StructuredProperty(Message)
	aQuery = ndb.StructuredProperty(adQuery) 

class adDbBuild(webapp2.RequestHandler):
	def get(self):
		a = q=Ad.query()
		a = a.fetch(1000)
		for ad in a:
			ad.put()
		self.response.write(errorPage('ad Database built'))
					
class MessageHandler(webapp2.RequestHandler):
    def get(self):
		logging.info("message handler")
		conv_query = Conversation.query().order(Conversation.message.date)	
		#mess_query = Message.query()
		#self.response.write(MESSAGE_PAGE_HTML)
		user_id = self.request.cookies.get('id')
		st = Student.query(Student.user_id==user_id).get() 
		page = buildStudentOffersPage(conv_query,st.google_id)
		"""
		for conver in conv_query:
			for message in conver.message:
				if(message.receiver == users.get_current_user().nickname()):
					send = users.User(_user_id = message.sender.identity)
					self.response.write('<p>recieved: %s</p>' %message.date)
					self.response.write('<p>from: %s</p>' %send.nickname())
					self.response.write('<p>%s</p><br>' %message.cont)
					#self.response.write('<div><a href="/messageReply?%s">reply</a></div>' %conver.id)
	"""
		self.response.write(page)



class MessageSend(webapp2.RequestHandler):
	# def getEmail(self):
	# 	user_id = self.request.cookies.get('id')
	# 	student_query=Student.query(Student.user_id==user_id).get()
	# 	comapny_query=Company.query(Company.user_id==user_id).get()
	# 	if (student_query!=None):
	# 		email = student_query.email
	# 	elif (comapny_query!=None):
	# 		email = comapny_query.email
		
	# 	logging.info("getEmailResult:"+email)
	# 	self.response.write('getEmailResult is:' + email+'\n')
	# 	return email
	
	
	def post(self):
		#self.conNum = threadNum(num=0)
		#self.conNum.put()
		ad_id = self.request.get('ad_id')
		logging.info(ad_id)
		user_id = self.request.cookies.get('id')
		comp = Company.query(Company.user_id == user_id).get()
		if (int(ad_id)!=-1):
			email = comp.email
			ad_query = Ad.query(Ad.message.compMail == email).order(Ad.message.date).fetch()
			#ad_query = Ad.query(Ad.user_id ==user_id).fetch()
			self.ad = ad_query[int(ad_id)]
		
		compName = self.request.get('companyName')
		compCity = self.request.get('companyCity') 
		comp.city = compCity
		comp.name = compName
		comp.put()
		
		recList = self.request.get_all('studentselect') 
		destAdd = self.request.get('recv') + "@example.com"
		#destId = users.User(destAdd)
		#logging.info(len(recList))
		#destIdKey = destId.put()
		#destIdVal = destIdKey.get()
		#self.key = appUser(usr=destId).put()
		#self.rec = self.key.get()
		logging.info("starting message sending proccess " + str(len(recList)))
		for rec in recList:
			st = Student.query(Student.user_id==rec).get()
			self.conversation = Conversation()
			self.message = Message(cont = self.request.get('note'))
			#self.message.receiver = Author(identity = rec)
			self.message.receiver = Author(identity = st.google_id)
			self.message.compName = compName
			self.message.compLocation = compCity
			self.message.jobName = self.request.get('jobId')
			self.message.compMail = self.request.get('companyMail')
			self.message.date = datetime.datetime.now()
			#userid = self.request.cookies.get('id')
			cmp = (Company.query(user_id==Company.user_id)).get()
			#self.message.sender = Author(identity = userid)
			self.message.sender = Author(identity = cmp.google_id)
			
			# if the message was sent using an Ad update wich student recieve the message in the Ad structure.
			if (int(ad_id)!=-1):
				#self.ad.sentId.append(rec)
				self.ad.sentId.append(st.google_id)
				self.ad.put()
				
			#if users.get_current_user():
				#self.message.sender = Author(identity=users.get_current_user().user_id())
			
			self.conversation.message = [self.message]
		
			#conNum = threadNum.query().get()
			#self.conversation.id = conNum.num
			#conNum.num +=1
			#conNum.put()
			self.conversation.put()
			self.message.put()
			logging.info("message inserted")
			
			student=Student.query(Student.user_id==rec).get()
			if student.allow_emails==True:
				user_address=student.email
				
				if not mail.is_email_valid(user_address):
					self.response.write("Error: student email address is not valid!")
				else:
					sender_address = "TauHireTeam@gmail.com"
					subject = "TauHire team - New Message Notification"
					# body = """ Dear Sir/Madam, \n \n 
					# You have a new Job Offer in TauHire website, \n \n 
					# Please visit our site to view your messages, \n \n 
					# Best regards, \n \n TauHire team"""
					body = "Dear Sir/Madam,\n\n"+"You have a new message in TauHire website: \n \n" + \
					"From: "+ self.message.compName + "\n\n"+"Company mail: "+ self.message.compMail+"\n\n"+\
					"Job name: "+ self.message.jobName+ "\n\n"+"Message content: "+ self.message.cont+"\n\n"+\
					"Best regards"+"\n\n"+"TauHireTeam"

					mail.send_mail(sender_address, user_address, subject, body)
					#self.response.write("mail was good")

		# cours_query = Course.query()
		# page = buildCompanyQuery(cours_query)
		# self.response.write(page)
		user_id = self.request.cookies.get('id')
		if (Company.query(user_id==Company.user_id).get()==None):
			self.response.write(errorPage("You are no longer connected! Please try to connect again"))
		else:
			comp = Company.query(Company.user_id == user_id).get()
			email = comp.email
			
			#ad_query = Ad.query(Ad.user_id ==user_id )
			ad_query = Ad.query(Ad.message.compMail == email).order(Ad.message.date).fetch()
			page = buildCurrentAdsPage(ad_query)
			self.response.write(page)

		self.response.write("""<html>
									<link rel="stylesheet" type="text/css" href="companyQueryFormPage/style.css">

									<body>
										
									</body>

	<script type="text/javascript" src="StudentWelcomePage/script.js"></script>
	<div class="popup" data-popup="popup-1">
    <div class="popup-inner">
        <h2 class="txt">message was sent successfully!</h2>
		
        <a class="popup-close" data-popup-close="popup-1" href="#">x</a>
    </div>
</div>

		<a class="btn" hidden data-popup-open="popup-1" href="#">Open Popup #1</a>
														

									</html>""")


#class MessageReply(webapp2.RequestHandler):
	#def get(self):
		#self.response.write(MESSAGE_PAGE_HTML)
		
	#def post(self):
		#self.message = Message(cont = self.request.get('mess'))

# this function insert a new ad or an edit of existing ad to the database
# a case of new ad is marked with ad_id = -1
class adHandler(webapp2.RequestHandler):
	
	def post(self):
		ad_id = self.request.get('ad_id')
		user_id = self.request.cookies.get('id')
		comp_query = Company.query(Company.user_id ==user_id).get()
		
		#collecting parameters from the html form
		course_names=self.request.get_all('name')
		grade = self.request.get_all('grade')
		average=self.request.get('avg')
		
		logging.info("number of grades received " + str(len(grade)))
		logging.info("number of courses received " + str(len(course_names)))
		
		#if there is no average in the input - place 60  
		if(average==""):
			average = 60
			
		crstypes=self.request.get_all("ctype")
		crstype_avgs=self.request.get_all("ctype_avg")
		residence=self.request.get("residence")
		year=self.request.get("year")
		availability=self.request.get("availability")
		adCont = self.request.get("note")
		adName = self.request.get("jobId")
		searchTerms = self.request.get('searchBar')
		
		# convert search query string into list (with input validation to make sure input is number or a letter)
		srcWordList = re.sub("~/[\p{L}]/", " ",  searchTerms).split()
		logging.info(srcWordList)
		
		# if the ad is a new ad
		if (int(ad_id)==-1):
			logging.info("ad id = -1")
			self.ad = Ad()
			self.ad.sentId = []
		else:
			adqy = Ad.query(Ad.message.compMail == comp_query.email).order(Ad.message.date).fetch()
			#adqy = Ad.query(Ad.user_id ==user_id ).fetch()
			self.ad = adqy[int(ad_id)]
		
		dbHandler = db.dbHandler()
		stdCrs= dbHandler.createStudentCourse(course_names, grade)
		
		#creating adQuery
		self.qry = adQuery()
		self.qry.student_courses=stdCrs
		self.qry.cgrades = grade
		self.qry.avg= int(average)
		self.qry.ctypes = crstypes 
		self.qry.ctype_avgs=crstype_avgs
		self.qry.residence= int(residence)
		self.qry.availability= int(availability)
		self.qry.year= int(year)
		self.qry.hasGit= "False"
		self.qry.srchWords = srcWordList
		
		if (self.request.get('getEmailNotification')=="True"):
			self.qry.scheduler=True
		else:
			self.qry.scheduler=False
		
		#creating message
		self.message = Message(cont = adCont)
		self.message.jobName = adName
		self.message.compMail = comp_query.email
		self.message.compName = comp_query.name
		
		self.ad.user_id = comp_query.google_id
		self.ad.message = self.message
		self.ad.aQuery = self.qry
		
		#studnum is a parameter that save the number of students the company has seen in the ad results
		if (int(ad_id)==-1):
			self.ad.studNum = "0" 		
		ad_key = self.ad.put()
		t.sleep(1)
		
		#comp = Company.query(Company.user_id == user_id).get()
		#email = comp.email
		ad_query = Ad.query(Ad.message.compMail ==  comp_query.email).order(Ad.message.date).fetch()
		#ad_query = Ad.query(Ad.user_id ==user_id).fetch()
		
		#this loop is used to find new ad and to redirect the user to the ad results
		i = 0 
		for ad in ad_query:
			#logging.info(ad.key.id())
			if (ad.key.id() == ad_key.id()):
				logging.info("i " + str(i))
				break
			i+=1
			
		#if ad is new redirect to ad results otherwise redirect to ad list	
		if (int(ad_id)==-1):	
			self.redirect("/showAdResults?ad_id=" + str(i))
		else:
			self.redirect("/currentAds")
		

# class ConfirmUserSignup(webapp2.RequestHandler):
#     def post(self):
#     	user_address = self.request.get('companyMail')
#     	#self.response.write('mail is:' + user_address)
#     	logging.info(user_address)
#         if not mail.is_email_valid(user_address):
#             self.response.write("please enter valid email address, please please please!!!")
#         else:
#         #sender_address = "Example.com Support <support@example.com>"
#         	sender_address = "support@example.com"
#         	subject = "Confirm your registration"
#         	body = """ I'm in! Yalla Macabi!!!!!!!!!!!!!!!!!!!!!!!!! """
#         	mail.send_mail(sender_address, user_address, subject, body)
#         	self.response.write("mail was good")
