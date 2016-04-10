import cgi
import urllib
import datetime
from methods import *

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import logging

#DB class definitions:

class Course(ndb.Model):
	"""Sub model for representing a course."""
	course_id = ndb.StringProperty(indexed=True, required=True)
	course_name = ndb.StringProperty(indexed=True, required=True)
	course_type = ndb.StringProperty(indexed=False, required=True)

class Student_Course(ndb.Model):
	grade = ndb.IntegerProperty(indexed=True, required=True)
	#weight = ndb.IntegerProperty(indexed=False, required=True)
	#semester = ndb.StringProperty(indexed=False, required=True)
	course= ndb.StructuredProperty (Course, required=True)
	#hashed_id = ndb.IntegerProperty(indexed=False)
	
	
class Student(ndb.Model):
	id = ndb.StringProperty(indexed=True, required=True)
	name= ndb.StringProperty(indexed=True, required=True)
	city =ndb.StringProperty(indexed=True, required=True)
	student_courses=ndb.StructuredProperty(Student_Course,repeated=True)	


	
class minGradeQuery(webapp2.RequestHandler):
	def post(self):	 
		course_names=self.request.get_all('name')
		grades= self.request.get_all('grade')
			
		#c=Course(course_name=course_name[0], course_id="1", course_type="class")		
		self.response.write('<html><body>')
		#debug prints
		self.response.write(int(grades[0]))
		#self.response.write(int(grades[1]))
		self.response.write("<br>End of Debug prints<br><br>")
		q=Student.query()
		for i in range (0,len(grades)-1):	
			logging.info(i)
			grade=int(grades[i])
			q=q.filter (Student.student_courses.grade>=grade, Student.student_courses.course.course_name==course_names[i])
		self.response.write(q)
		## TODO: write the response in a nicer way
		q.fetch(100)
		#for student in q:
		#	self.response.write("""<br> <h1 style="color:red">Student %s <br>""" %student)
		#self.response.write('End of Results</html></body>')
		page = buildQueryResultsPage(q)
		self.response.write(page)

#adds all courses to DB from the parsed courses files
class dbBuild(webapp2.RequestHandler):
	
	def get(self):
		inputfile=open("courses.csv")
		text = inputfile.readlines()
		for i in range(0,len(text)-2,2):
			c=Course(course_name=text[i],course_id=text[i+1], course_type="class")
			c.put()
			
		inputfile.close()
		self.response.write('Database built')

#deletes all courses from DB	
class dbDelete(webapp2.RequestHandler):

	def get(self):
		ndb.delete_multi(Course.query().fetch(keys_only=True))
		self.response.write('Database deleted')

#adds Student_Course to DB
class dbHandler(webapp2.RequestHandler):
    def post(self):	 
		self.response.write('<html><body>Test Entry ')
		self.response.write(self.request)
		course_names=self.request.get('name', allow_multiple=True)
		self.response.write("<br><br>")
		
		grade= self.request.get('grade', allow_multiple=True)
		if (len(course_names)!=len(grade)):
			self.response.write ("Error")
		s=[]
		for i in range(0,len(course_names)):
			c=Course(course_id='1', course_name=course_names[i], course_type="class")
			s.append(Student_Course(grade=int(grade[i]), course=c))
		st= Student(student_courses=s,id="2", name="demo", city="demo")
		st.put()
		## TODO: write the response in a nicer way
		self.response.write('<html><body>Test Entry added</body></html>')

#classes that send pages to user, should check if the duplicates can be reduced
