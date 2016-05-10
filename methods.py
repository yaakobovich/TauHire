#!/usr/bin/python
# -*- coding: utf-8 -*-

#important to support utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import cgi
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb

#Methods to build the companyQueryResultsPage and StudentOffersPage

def buildQueryResultsPage(q):
	i=0
	
	htmlstart= """<!DOCTYPE html>
	<html>
	<link rel="stylesheet" type="text/css" href="companyQueryResultsPage/style.css">
	<body>
	
  <div align="right">
    <p class="titletext">:שליחת משרה</p>
  </div>

  <div id="form-div">
    <div align="right"> <p class="medtitletext">:הזן משרה</p>  </div>
    <form class="form" id="form1" action="/messageSend" method="post">
      <div align="right">
        <p class="text1">:שם החברה</p>
        <input name="companyName" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder="שם" id="companyName" />
      </div>

      <div align="right">
        <p class="text1">:מייל החברה</p>
        <input name="companyMail" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder="מייל" id="name" />
      </div>

      <div align="right">
        <p class="text1">:שם המשרה</p>
        <input name="jobId" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder="משרה" id="jobId" />
      </div>

      <div align="right">
        <p class="text1">:תיאור המשרה</p>
        <textarea class="scrollabletextbox" name="note" dir="rtl" placeholder="פרטים על המשרה.."></textarea>
        
           
      </div>
	<div align="right" > <p class="medtitletextpadded">:בחר מועמדים</p> </div>

      <div id="scroll" style="overflow-y: scroll; height:450px;">"""
	  
	htmlbody=''
	hasCv=False
	for student in q:
		i=i+1
		hasCv=False
		if (student.cv_blob_key != None) :
			hasCv=True
		
		if (hasCv) :
			htmlbody+="""
			<div class="form-element" ; align="right">
			  <label for="studentselect"""+str(i)+"""" class="textsmallpad">בחר</label>
			  <input type="checkbox" name="studentselect" id="studentselect" """+str(i)+""" class="checkbox" 
			  value="""+str(student.user_id)+""">
			  <button type="button" onclick="location.href='getCV?user_id="""+str(student.user_id)+ """'" id="Cvbutton" """+str(i)+""" class="Cvbutton">הצג</button>
			  <p class="textbigpad">:קורות חיים</p>
			  <p class="text" >"""+student.city.decode('utf-8', 'ignore')+"""</p>
			  <p class="text">:עיר</p>
			</div>"""
		else :
			htmlbody+="""

			<div class="form-element" ; align="right">

			  <label for="studentselect"""+str(i)+""" class="textsmallpad">בחר</label>
			  <input type="checkbox" name="studentselect" id="studentselect" """+str(i)+""" class="checkbox" 
			  value="""+str(student.user_id)+""">
			  <p class="textbigasCvButton">לא צורף</p>
			  <p class="textbigpad">:קורות חיים</p>
			  <p class="text" >"""+student.city.decode('utf-8', 'ignore')+"""</p>
			  <p class="text">:עיר</p>

			</div>"""		
	
	htmlend="""
      </div>

      <label for="select-all" class="textsmallpad">בחר הכל</label>
      <input type="checkbox" name="select-all" id="select-all" />
      <div class="submit">
        <input type="submit" value="שלח משרה" id="button-blue" />

      </div>
    </form>

  </div>
  </body>
  	<script type="text/javascript" src="/jquery/jquery-2.2.3.js"></script>
	<script type="text/javascript" src="/toolbar/loadtoolbar.js"></script>
	<script type="text/javascript" src="companyQueryResultsPage/script.js"></script>
	
	</html>"""

	html=htmlstart+htmlbody+htmlend
	return html
		
def buildStudentOffersPage(conv_query, user_id):
	i=0
	htmlstart= """<!DOCTYPE html>
	<html>
	<link rel="stylesheet" type="text/css" href="StudentOffersPage/style.css">
	<body>
  <div >
    <p class="titletext"  >:ההצעות שלי</p>
  </div>

  <div id="form-div">
    <div align="right"> <p class="medtitletext">:הצעות שקיבלת</p>  </div>
  


      <div id="scroll">"""
	  
	htmlbody=''
	
	for conver in conv_query:
		for message in conver.message:
			if(message.receiver.identity == user_id):
				#send = Student.query(Student.id==message.sender.identity).get()
				#send = users.User(_user_id = message.sender.identity)
				i=i+1
				htmlbody+="""

				        <div class="form-element" ; align="right">
		
						<div align="right">
							<button type="button" id="button"""+str(i)+"""" class="button">הצג פרטים</button>
							<p class="text">"""+str(message.compMail)+"""</p>
							<p class="text">:מייל</p>
							<p class="text">"""+str(message.compName)+"""</p>
							<p class="text">:שם חברה</p>
							<p class="text">"""+str(message.jobName)+"""</p>
							<p class="text">:שם משרה</p>
						</div>
				
						<div class="form-extra" id="extra"""+str(i)+"""""; align="right">

						<p class="text" id="extra1" >""" +str(message.cont)+ """</p>


						</div>
				</div>"""
	
	emptypage="""
            </div>

    <div align="right"> <p class="medtitletext" id="empty">...טרם קיבלת הצעות</p>  </div>

  </div>"""

	htmlend = """
  </body>
	<script type="text/javascript" src="StudentOffersPage/jquery-2.2.3.js"></script>
	<script type="text/javascript" src="StudentOffersPage/script.js"></script>
	<script type="text/javascript" src="/toolbar/loadtoolbar.js"></script>
	</html>"""

	html=htmlstart+htmlbody+htmlend
	return html


def buildStudentInputPage(course_query):
	i=0
	htmlstart="""<!DOCTYPE html>
	<html lang="he">
		<link rel="stylesheet" type="text/css" href="studentInputPage/style.css">
<script type="text/javascript" src="studentInputPage/jquery-2.2.3.js"></script>

	  <body>
<script type="text/javascript" src="/toolbar/loadtoolbar.js"></script>
	  <div id="form-main">
		<div align="right">
		  <p class="titletext">:הרשמה</p>
		</div>
		<div id="form-div">
		  <div align="right">
		    <p class="text1">:הזן עיר מגורים</p>
		  </div>
		<form class="form" id="form1" action="/dbHandler" method="post" onsubmit="return validateForm()" enctype="multipart/form-data">
		  <input name="city" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder="עיר" id="city" />
		  <div align="right">
		    <p class="text1">:הזן קורסים וציונים</p>
		  </div>
		  
		    <div class="inputline">
		      <input type="button" id="buttonadd" value="הוסף קורס" />
		    </div>
		    <div id="cloneme0" class="cloneme">
		      <input name="name" type="text" list="courses" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input" placeholder="שם קורס" id="name" autocomplete="off"/>
		      <input name="grade" type="number" class="validate[required,custom[email]] feedback-input2" min="60" max="100" id="grade" placeholder="ציון" />
		      <input type="button" id="buttondel0" class="buttondel" value="X" />
			  
		    </div>
		
		
		
		    <div align="right" id=cventry>
		      <p class="text1" >:אופציונלי-הזן קורות חיים</p>
		    </div>

		    <input name="cv" type="file" accept=".pdf,.doc,.txt,.docx" id="cv" />

		    <div align="right" id=avgEntry>
		      <p class="text1" >:אופציונלי-הזן ממוצע כללי</p>
		    </div>
		    <div id="cloneme0" class="cloneme">
		      <input name="average" type="number" class="validate[required,custom[email]] feedback-input2" min="60" max="100" id="average" placeholder="ממוצע" />			  
		    </div>
		
		    <div class="submit">
		      <input type="submit" value="שלח" id="button-blue" />
		      <div class="ease"> </div>
		    </div>
			<datalist id="courses" hidden>"""
	htmlbody=''
	
	for course in course_query:
		i=i+1
		htmlbody+="""<option> """+  str(course.course_name) + """</option> data-id="1" """
		
	htmlend="""</datalist>
		  </form>
		</div>
		<div class="validation-result hidden"></div>
			
		
	  </div>

	  </body>


		<script type="text/javascript" src="studentInputPage/script.js"></script>

	</html>
"""

	html=htmlstart+htmlbody+htmlend
	return html

def buildCompanyQuery(course_query):
	i=0
	htmlstart="""<!DOCTYPE html>
	<html>
		<link rel="stylesheet" type="text/css" href="companyQueryFormPage/style.css">
	  <body>
		
		<div id="form-main">
		<div align="right">
		  <p class="titletext">:סינון מועמדים</p>
		</div>
		<div id="form-div">

		  <div align="right">
			<p class="text1">:ציון מינימלי בקורס</p>
		  </div>
		  <form class="form" id="form1" action="/companyQueryResultsPage" method="post">

			<div class="inputline">
			  <input type="button" id="buttonadd" value="הוסף קורס" />
			</div>
			<div id="cloneme0" class="cloneme">
			  <input name="name" type="text" list="courses" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input" placeholder="שם קורס" id="name" />
			  <input name="grade" type="number" class="validate[required,custom[email]] feedback-input2" min="60" max="100" id="grade" placeholder="ציון" />
			  <input type="button" id="buttondel0" class="buttondel" value="X" />
			</div>
			<div align="right" id="bysubject">
			  <p class="text1">:ממוצע מינימלי באשכול</p>
			</div>
			<div class="inputline">
			  <input type="button" id="buttonaddtwo" value="הוסף אשכול" />
			</div>
			<div id="clonemetwo0" class="clonemetwo">
			  <select name="ctype" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input" placeholder="שם אשכול" id="ctype">
				<option value=0>(לא נבחר אשכול)</option>
			  <option value=1>מתמטיקה</option>
				<option value=2>תכנות</option>
				<option value=3>תאוריות מדעי המחשב</option>
				<option value=4>אבטחת מידע</option>
				<option value=5>מדעי המידע</option>
				<option value=6>רשתות</option>
				<option value=7>ביואינפורמטיקה</option>



			  </select>



			  <input name="ctype_avg" type="number" class="validate[required,custom[email]] feedback-input2" min="60" max="100" id="ctype_avg" placeholder="ממוצע" />
			  <input type="button" id="buttondeltwo0" class="buttondeltwo" value="X" />
			</div>
			<div align="right" id=avgentry>
			  <p class="text1">:ממוצע תואר מינימלי</p>
			  <input name="avg" type="number" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" min="60" max="100" placeholder="ממוצע" id="avg" />
			</div>
			<div class="submit">
			  <input type="submit" value="חפש" id="button-blue" />
			  <div class="ease"></div>
			</div>
			<datalist id="courses" hidden>"""
	htmlbody=''
	
	for course in course_query:
		i=i+1
		htmlbody+="""<option> """+  str(course.course_name) + """</option data-id="1"> """
		
	htmlend="""</datalist>
		  </form>
		</div>
		
				
				
				
	  </div>
		<script type="text/javascript" src="/jquery/jquery-2.2.3.js"></script>
		<script type="text/javascript" src="/toolbar/loadtoolbar.js"></script>
		<script type="text/javascript" src="/companyQueryFormPage/script.js"></script>
	  </body>
	  
	  </html>"""

	html=htmlstart+htmlbody+htmlend
	return html

def buildStudentEditPage(student):
	htmlstart="""﻿<!DOCTYPE html>
<html lang="he">
	<link rel="stylesheet" type="text/css" href="studentEditPage/style.css">
  <body>
  <div id="form-main">
    <div align="right">
      <p class="titletext">:הפרטים שלי</p>
    </div>
    <div id="form-div">
      <div align="right">
        <p class="text1">:עיר מגורים</p>
      </div>
	<form class="form" id="form1" action="/dbHandler" method="post">
      <input name="city" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder='""" + str(student.city) + """'align "right" id="city" />
      <div align="right">"""

	htmlbody = """<p class="text1">:הקורסים שלי</p>
      </div>
		<div class="inputline">
          <input type="button" id="buttonadd" value="הוסף קורס" />
        </div>"""
	for crs in student.student_courses:
		htmlbody+= """
        <div id="cloneme0" class="cloneme">
          <input name="name" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input" placeholder='""" + str(crs.course.course_name) + """' id="name" />
          <input name="grade" type="number" class="validate[required,custom[email]] feedback-input2" min="60" max="100" id="grade" placeholder='""" + str(crs.grade) + """' />
          <input type="button" id="buttondel0" class="buttondel" value="X" /< </div>
		<div align="right" id=cventry>"""
		


	if (student.cv_blob_key != None) :
			hasCv=True
	htmcv = """<p class="text1" >:קורות חיים</p>
        </div>
		<div align="right">
		<input name="cv" type="file" id="cv" />"""
	if(hasCv):	
		htmcv += """<button type="button" onclick="location.href='getCV?user_id="""+str(student.user_id)+ """'" id="Cvbutton" class="Cvbutton">הצג</button>
         </div>"""



	htmend = """<div class="submit">
          <input type="submit" value="שמור" id="button-blue" />
          <div class="ease"> </div>
        </div>
      </form>
    </div>
		<script type="text/javascript" src="studentEditPage/jquery-2.2.3.js"></script>
	<script type="text/javascript" src="studentEditPage/script.js"></script>
  </div>

  </body>

</html>"""
	

	html=htmlstart + htmlbody + htmcv + htmend
	return html
