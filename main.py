from PyQt4 import QtGui, QtCore,uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3,os
import loginpage, part1result
import random, Final_result,euler
#import httplib2
import urllib2,cookielib
#import requests

f_skipcnt=3
ans=0
scrA=0
scrB=0
reccount = 0
recno=0
past_recno=0
timeflagA=0
timeflagB=0
timeflagC=0
timeflagD=0
timestr=900
timestrB = 600
past_cnt=0
present_cnt=0
present_recno=0
rcptno=""
txtbwsr=30
year=2014
f_recno=0
skipcount=3
tablename=''
q_cnt=0
past_q=[]
usr_q=''
ans_list=''
q_list=[]
nm1=''
nm2=''
colgname=''
resp_list=''
past_recno=0
pq_list=[]
pastusr_q=''
pastans_list=''
pastq_list=[]
present_recno=0
presentusr_q=''    # to store the list of present questions sep @ in db later
presentans_list=''
f_anslist=''
fq_list=[]
fq=''
p=""

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)




conn = sqlite3.connect('clash14.db')
mcq_class = uic.loadUiType("exp.ui")[0]

class Window(QtGui.QMainWindow,mcq_class):

   #Main_Class Initialisation function
   def __init__(self):
      #print "init"
      QtGui.QMainWindow.__init__(self)
      self.login()
   #login function to render the login page
   def login(self):
     #print "login"
     self.Form=QtGui.QMainWindow()
     self.ui=loginpage.Ui_MainWindow()
     self.ui.setupUi(self.Form)
     self.Form.showFullScreen()
     self.ui.loginbutton.clicked.connect(self.logincheck)

   #logincheck function to validate and store login details to database
   def logincheck(self):
      #print "logincheck"
      global timeflagA,timeflagB,timeflagC,timeflagD,rcptno,tablename,nm1,nm2,colgname,rnd,reccount,f_count,p
      flag=0
      rcptno=self.ui.rno.text()
      c_rcpt=self.ui.crno.text()
      nm1=self.ui.name1.text()
      nm2=self.ui.name2.text()
      colgname=self.ui.colg.text()
      mobile=self.ui.mob.text()
      rnd = "*"
      
      nm1=str(nm1)
      nm1.replace(" ","")
      nm1=str(nm1)
      nm2= nm2.replace(" ","")
      colgname=str(colgname)
      colgname = colgname.replace(" ","")
      mobile=str(mobile)
      mobile.strip()
      rcptno=str(rcptno)
      rcptno.strip()
      c_rcpt=str(c_rcpt)
      c_rcpt.strip()
      
      l=len(str(mobile))
      if self.ui.junior.isChecked()==1:
         rnd="J"
         
      elif self.ui.senior.isChecked()==1:
         rnd="S"
      if (str(rcptno)=='') | (str(nm1)=='') | (str(nm2)=='') | (str(colgname)=='') | (str(mobile)=='') | (rnd=='*'):
         QMessageBox.about(self,'Clash','Fill all Details!')
         flag=1
      if (str(rcptno)) <> (str(c_rcpt)):
         QMessageBox.about(self,'Clash','Receipt Numbers should match!')
         flag=1
      if ((str(mobile)).isdigit()==0) | l!=10:
         QMessageBox.about(self,'Clash','Mobile Number must be numeric and 10 digit!')
         flag=1
      if timeflagA==1:
         QMessageBox.about(self,'Clash','Time is up!')
         flag=1
      
      part_cur = conn.execute(str("SELECT Part FROM FlagDB WHERE R_No ="+rcptno+" "))
      part = part_cur.fetchone()
      if part:
         p = str(part[0])
      else:
         p="A"
      print "upper"+p
      if flag==0:
         try:
            #print "try"
             if (rnd == "J"):
                tablename = "Juniors"
             elif (rnd =="S"):
                tablename = "Seniors"
             sqlstr1 = "INSERT INTO LoginDB (Receipt_No, Name1, Name2, College, Mobile, Round) VALUES(" + rcptno +",'" +  nm1 + "','" + nm2 + "','" +  colgname + "','" + mobile + "','" +  rnd  + "')"
             sqlstr3 = "INSERT INTO ServerDB (R_No,Name1,Name2,College,round) VALUES(" + rcptno +",'" +  nm1 + "','" + nm2 + "','" +  colgname +"','"+ rnd+ "')"
             conn.execute(str(sqlstr1))
             conn.execute(str(sqlstr3))
             conn.commit()
             cursor = conn.execute("SELECT count(*)  from '"+tablename+"'")
             row = cursor.fetchone()
             reccount = row[0]

             cursor1 = conn.execute("SELECT count(*)  from EulerQuestionDB")
             rows = cursor1.fetchone()
             f_count = rows[0]

             conn.execute(str("INSERT INTO FlagDB (R_No,Part) VALUES ("+rcptno+",'A')"))
             conn.commit()
             self.mcq()
         except:
           #print "except"

            
           #print p
            
            time_curA = conn.execute(str("SELECT Timer_A FROM UserMcqDB WHERE R_No="+rcptno+""))
            tmA = time_curA.fetchone() 
            time_aa=int(tmA[0])
            print time_aa
            
            time_curB = conn.execute(str("SELECT Timer_B FROM Part2_DB WHERE R_No="+rcptno+""))
            tmB = time_curB.fetchone() 
            if tmB:
               time_bb = int(tmB[0])
            else:
               time_bb = 0
            print time_bb
            print p
            if(time_aa<>0 or time_bb!=0): 
               if p == "A":
                   #time_cur = conn.execute(str("SELECT Timer_A FROM UserMcqDB WHERE R_No="+rcptno+""))
                   #tm = time_cur.fetchone()
                   timeA = time_aa
                   if timeA == 0 :
                       timeflagA = 1
                       timeflagB = 0
                       timeflagC = 0
                       timeflagD = 0
                   if timeflagA <> 1:
                      #print "except1"
                       sqlstr2 = "UPDATE LoginDB SET Receipt_No="+ rcptno+", Name1='"+ nm1+"',Name2='" + nm2 +"',College='" + colgname +"',Mobile='" + mobile  + "',Round = '" +rnd +"' WHERE Receipt_No="+ rcptno+" "
                       conn.execute(str(sqlstr2))
                       conn.commit()
                       if (rnd == "J"):
                           tablename = "Juniors"
                       elif (rnd =="S"):
                           tablename = "Seniors"
                       cursor = conn.execute("SELECT count(*)  from '"+tablename+"'")
                       row = cursor.fetchone()
                       reccount = row[0]
         
                       self.restartA()
                   
               elif p == "B":
                  
                  #print "except2"
                   #time_cur = conn.execute(str("SELECT Timer_B FROM Part2_DB WHERE R_No="+rcptno+""))
                   #tm = time_cur.fetchone()
                   #print tm
                   timeB = time_bb
                   print timeB
                   if timeB == 0 :
                       timeflagA = 0
                       timeflagB = 1
                       timeflagC = 0
                       timeflagD = 0
                   if timeflagB <> 1:
                       sqlstr2 = "UPDATE LoginDB SET Receipt_No="+ rcptno+", Name1='"+ nm1+"',Name2='" + nm2 +"',College='" + colgname +"',Mobile='" + mobile  + "',Round = '" +rnd +"' WHERE Receipt_No="+ rcptno+" "
                       conn.execute(str(sqlstr2))
                       conn.commit()
                       if (rnd == "J"):
                           tablename = "Juniors"
                       elif (rnd =="S"):
                           tablename = "Seniors"
                       self.restartB()


               elif p == "C":
                  #print "except3"
                   #time_cur = conn.execute(str("SELECT Timer_B FROM Part2_DB WHERE R_No="+rcptno+""))
                   #tm = time_cur.fetchone()
                   #print tm
                   timeC = time_bb
                   if timeC == 0 :
                       timeflagA = 0
                       timeflagB = 0
                       timeflagC = 1
                       timeflagD = 0
                   if timeflagC <> 1:
                       sqlstr2 = "UPDATE LoginDB SET Receipt_No="+ rcptno+", Name1='"+ nm1+"',Name2='" + nm2 +"',College='" + colgname +"',Mobile='" + mobile  + "',Round = '" +rnd +"' WHERE Receipt_No="+ rcptno+" "
                       conn.execute(str(sqlstr2))
                       conn.commit()
                       if (rnd == "J"):
                           tablename = "Juniors"
                       elif (rnd =="S"):
                           tablename = "Seniors"
                       self.restartC()
               elif p == "D":
                  #print "except4"
                   #time_cur = conn.execute(str("SELECT Timer_B FROM Part2_DB WHERE R_No="+rcptno+""))
                   #tm = time_cur.fetchone()
                   #print tm
                   timeD = time_bb
                   if timeD == 0 :
                       timeflagA = 0
                       timeflagB = 0
                       timeflagC = 0
                       timeflagD = 1
                   if timeflagD <> 1:
                       sqlstr2 = "UPDATE LoginDB SET Receipt_No="+ rcptno+", Name1='"+ nm1+"',Name2='" + nm2 +"',College='" + colgname +"',Mobile='" + mobile  + "',Round = '" +rnd +"' WHERE Receipt_No="+ rcptno+" "
                       conn.execute(str(sqlstr2))
                       conn.commit()
                   cursor1 = conn.execute("SELECT count(*)  from EulerQuestionDB")
                   rows = cursor1.fetchone()
                   f_count = rows[0]

         
                   self.restartD()

            else:
               #print "except5"
                QMessageBox.about(self,'Clash','Time up!')
                exit()
                
   #mcq function to show the MCQ page with timer and score   
   def mcq(self):
     #print "mcq"
      self.Form.hide()
      #self.ui.loginbutton.setEnabled(False)
      global reccount,timestr,usr_q,ans_list,q_list,past_q,past_cnt,tablename,q_cnt
      QtGui.QMainWindow.__init__(self)
      self.setupUi(self)
      self.showFullScreen()

      self.showque()
      self.skipcnt.display(skipcount)
      self.skipbutton.clicked.connect(self.skipit)
      self.nextbutton.clicked.connect(self.anscheckA)
      
     #print "mcq-timer part"
      self.timerA.display(timestr)
      self.timer = QTimer(self)
      self.timer.timeout.connect(self.TimerTickA)
      self.timer.start(1000)


   def skipit(self):
     #print "skipit"
      global skipcount
      if skipcount==0:
         QMessageBox.about(self,'Clash','Out of skips')
         self.skipbutton.setEnabled(False)
         return
      else:
         skipcount-=1
         self.skipcnt.display(skipcount)
         self.randit()
         self.showque()

         
   def randit(self):
     #print "randit"
      global recno,reccount,q_list
      recno = random.randint(0, (reccount-1))
      flg1 = (recno+1) in q_list
      #if flg1 :
        #print "exists " , recno
      excnt = 0 
      while flg1 and (excnt < reccount):
         recno = random.randint(0, (reccount-1))
         flg1 = (recno+1) in q_list
         excnt += 1
        #print excnt , "---", recno
      if (excnt >= reccount-1) :
        #print "Stopping function " 
         self.options()
      #print "q_id = " , recno
      

   #TimerTick function to display countdown timer
   def TimerTickA(self):
     #print "timerA"
      global timestr,timeflag,rcptno
      if timestr==0:
         #timeflagA=1
         self.timer.stop()
         self.options()
      else:
         global usr_q,ans_list
         timestr -= 1
         self.timerA.display(timestr)
         if ((timestr%5)==0):
            sqlstr1 = "INSERT OR IGNORE INTO UserMcqDB (R_No, Questn_List,Timer_A,Score_A,Ans_A) VALUES("+ rcptno+",'"+ usr_q+"'," + str(timestr) +"," + str(scrA) +",'" +  ans_list + "')"
            conn.execute(str(sqlstr1))
            conn.commit()
            sqlstr2 = "UPDATE UserMcqDB SET R_No="+ rcptno+", Questn_List='"+ usr_q+"',Timer_A=" + str(timestr) +",Score_A=" + str(scrA) +",Ans_A='" +  ans_list + "' WHERE R_No="+ rcptno+" "
            conn.execute(str(sqlstr2))
            conn.commit()
            sqlstr3 = "INSERT OR IGNORE INTO FlagDB (R_No, Q_List) VALUES("+ rcptno+",'"+ resp_list+"')"
            conn.execute(str(sqlstr3))
            conn.commit()
            sqlstr4 = "UPDATE FlagDB SET R_No="+ rcptno+", Q_List='"+ resp_list +"' WHERE R_No="+ rcptno+" "
            conn.execute(str(sqlstr4))
            conn.commit()

            #print "Success"
   
   def options(self):
      global rcptno,timestr,scrA,txtbwsr,p
     #print "options"
      self.timer.stop()
      self.hide()
      self.formres=QtGui.QWidget()
      self.uires=part1result.Ui_Form()
      self.uires.setupUi(self.formres)
      self.uires.scoreA.display(scrA)
      self.formres.showFullScreen()
      txtbwsr=30
      q_cnt=0
      print p
      if p=="A":
         print "past"+p
         self.uires.past_btn.clicked.connect(self.past_mcq)
         print "pres"+p
         self.uires.present_btn.clicked.connect(self.present_createlist)
         print "fut"+p
         self.uires.future_btn.clicked.connect(self.future)

   #showque function to show question with options on mcq page
   def showque(self):
     #print "showque"
      global reccount , recno, ans,rows,q_id,tablename
      if (recno < 0) :
         recno = 0
      if (recno >= reccount) :
        #print recno, reccount
         recno = reccount-1
         
         
      cursor = conn.execute("SELECT ques_id, ques, optA, optB, optC, optD, correctOpt  from '"+tablename+"' limit " + str(recno) + ",1")
      row = cursor.fetchone()
      #q_id=row[0]
      q_id = recno
      #print recno, q_id
      q= row[1] 
      op1= row[2]
      op2= row[3]
      op3= row[4]
      op4= row[5]
      ans = row[6]
     #print ans
      self.Question.clear()
      self.Question.append(q)
      self.Question.update()
      
      self.Opt_1.isChecked()==0
      self.Opt_2.isChecked()==0
      self.Opt_3.isChecked()==0
      self.Opt_4.isChecked()==0
      self.Opt_1.setAutoExclusive(0)
      self.Opt_1.setChecked(False)
      self.Opt_2.setAutoExclusive(0)
      self.Opt_2.setChecked(False)
      self.Opt_3.setAutoExclusive(0)
      self.Opt_3.setChecked(False)
      self.Opt_4.setAutoExclusive(0)
      self.Opt_4.setChecked(False)
      self.Opt_1.setAutoExclusive(1)
      self.Opt_2.setAutoExclusive(1)
      self.Opt_3.setAutoExclusive(1)
      self.Opt_4.setAutoExclusive(1)

      self.Op1.setWordWrap(True)
      self.Op2.setWordWrap(True)
      self.Op3.setWordWrap(True)
      self.Op4.setWordWrap(True)

      self.Op1.setText(op1)
      self.Op2.setText(op2)
      self.Op3.setText(op3)
      self.Op4.setText(op4)
      self.scoreA.display(scrA)
      
   #anscheck function to check answer and increment/decrement score and append to lists
   def anscheckA(self):
     #print "anscheckA"
      global ans,scrA,q_id,usr_q,ans_list,recno, reccount,q_list,past_q,past_cnt,txtbwsr,year,q_cnt,resp_list
      
      if self.Opt_1.isChecked()==0 and self.Opt_2.isChecked()==0 and self.Opt_3.isChecked()==0  and self.Opt_4.isChecked()==0:
         return
         
      q_cnt+=1
      option=''
      for radioButton in self.findChildren(QtGui.QRadioButton):
         if radioButton.isChecked():
            radioButtonText = str(radioButton.text())
            option = radioButtonText.strip()[0:1]
           #print "option"+str(option)
            if option == ans:
               scrA = scrA+4
               correct=1
               #past_q+='1'
               #past_q+='@'
               self.scoreA.display(scrA)
            else:
               scrA = scrA-2
               correct=0
               self.scoreA.display(scrA)
               past_cnt+=1
               past_q.append(q_id+1)
               resp_list+=(str(q_id+1))
               resp_list+=('@')
              #print resp_list
      if q_cnt ==29:
        self.options()
      usr_q+=(str(q_id+1))
      usr_q+=('@')
     #print usr_q
      q_list.append(q_id+1)
      #print q_list
               
      ans_list+=(option)
      ans_list+=('@')
     #print ans_list
      #print past_q

      self.randit()
      ansbox = self.findChild(QtGui.QTextBrowser, "ansbox_"+str(txtbwsr))
      
      if correct==1:
      	year+=1
      	ansbox.setStyleSheet(_fromUtf8("background-color : rgb(15,85,71)")) 
      else:
      	year-=1
      	ansbox.setStyleSheet(_fromUtf8("background-color : rgb(157,48,48)"))
      ansbox.append("<font color = white ><font size = 4> %s </font>" %  (str(year)) )
      txtbwsr -=1
      
      self.showque()

   def restartA(self):
     #print "restartA"
      global rcptno,timestr,scrA,q_list,usr_q,ans_list,recno
      resq_list=[]
      sqlstr1 = "SELECT R_No, Questn_List,Timer_A,Score_A,Ans_A FROM UserMcqDB WHERE R_No = "+rcptno
      rescur= conn.execute(str(sqlstr1))
      row = rescur.fetchone()
     #print row
      res_q = str(row[1])
      res_time = row[2]
      res_scr = row[3]
      res_ans = str(row[4])
      resq_list = res_q.split('@')
      del resq_list[0]
      del resq_list[-1]
     #print resq_list
      timestr = res_time
      usr_q=str(res_q)
      scrA=res_scr
      ans_list = str(res_ans)
      q_list = resq_list
      self.randit()
      self.mcq()




#--------------------------------------PRESENT-------------------------------------------------------------------
   def present_createlist(self):
      global q_list,present_q,present_recno,present_cnt,q_cnt,p
      if p=="B" or p=="D":
         return
      p="C"
      print p
      q_cnt=0
      present_q=range(2,328)
      present_cnt=30
      for q in q_list:
         if q in present_q:
            present_q.remove(q)
            del present_q[0]
      #print present_q
      #if p!="C":
      self.present_mcq()
      
      
#present_q=== list to fetch ques ids from
#present_recno== index from the present_q
   def present_mcq(self):
      print "present_mcq"
      #self.formres.hide()
      #self.uires.past_btn.setEnabled(False)
      #self.uires.present_btn.setEnabled(False)
      #self.uires.future_btn.setEnabled(False)
      global present_cnt,timestrB,presentusr_q,presentans_list,present_q,pq_list,present_recno,q_cnt,txtbwsr
      
      conn.execute(str("UPDATE FlagDB SET Part = 'C' WHERE R_No = "+rcptno+""))
      conn.commit()
      txtbwsr=30
      print txtbwsr
      QtGui.QMainWindow.__init__(self)
      self.setupUi(self)
      print txtbwsr
      self.showFullScreen()
      print txtbwsr
      self.showqueB_pres()
      print txtbwsr
      self.skipbutton.setEnabled(False)
      print str(timestrB)+"here"
      
      self.nextbutton.clicked.connect(self.anscheckB_pres)
      #print "present_mcq"

      self.timerA.display(timestrB)
      self.timer = QTimer(self)
      self.timer.timeout.connect(self.TimerTickB_pres)
      self.timer.start(1000)

   #TimerTick function to display countdown timer
   def TimerTickB_pres(self):
      global timestrB,timeflag,rcptno
     #print "TimerTickB_pres"
      if timestrB==0:
         self.timer.stop()
         self.hide()
         self.final_result()
      else:
         global presentusr_q,presentans_list,scrB
         timestrB -= 1
         self.timerA.display(timestrB)
         if ((timestrB%5)==0):
            sqlstr1 = "INSERT OR IGNORE INTO Part2_DB (R_No, Q_List,Timer_B,Score_B,Ans_B) VALUES("+ rcptno+",'"+ presentusr_q+"'," + str(timestrB) +"," + str(scrB) +",'" +  presentans_list + "')"
            conn.execute(str(sqlstr1))
            conn.commit()
            sqlstr2 = "UPDATE Part2_DB SET R_No="+ rcptno+", Q_List='"+ presentusr_q+"',Timer_B=" + str(timestrB) +",Score_B=" + str(scrB) +",Ans_B='" +  presentans_list + "' WHERE R_No="+ rcptno+" "
            conn.execute(str(sqlstr2))
            conn.commit()

            #print "Success"

   def showqueB_pres(self):
      print "showquesB_pres"
      
      global present_cnt , present_recno, present_ans,scrA,scrB,tablename,q_id,txtbwsr
      #print txtbwsr
      if (present_recno < 0) :
         present_recno = 0
      if (present_recno >= present_cnt) :
        #print present_recno, present_cnt
         present_recno = present_cnt-1
         
      #print present_q[present_recno]
      try:
         print tablename
         print present_q
         print present_recno
         presentcur = conn.execute("SELECT ques, optA, optB, optC, optD, correctOpt  from '"+tablename+"' WHERE ques_id="+str(present_q[present_recno])+"")
         row = presentcur.fetchone()
         q_id = present_q[present_recno]
         q= row[0]
         op1= row[1]
         op2= row[2]
         op3= row[3]
         op4= row[4]
         present_ans = row[5]
        #print present_ans
         self.Question.clear()
         self.Question.append(q)
         self.Question.update()
         self.Opt_1.isChecked()==0
         self.Opt_2.isChecked()==0
         self.Opt_3.isChecked()==0
         self.Opt_4.isChecked()==0
         self.Opt_1.setAutoExclusive(0)
         self.Opt_1.setChecked(False)
         self.Opt_2.setAutoExclusive(0)
         self.Opt_2.setChecked(False)
         self.Opt_3.setAutoExclusive(0)
         self.Opt_3.setChecked(False)
         self.Opt_4.setAutoExclusive(0)
         self.Opt_4.setChecked(False)
         self.Opt_1.setAutoExclusive(1)
         self.Opt_2.setAutoExclusive(1)
         self.Opt_3.setAutoExclusive(1)
         self.Opt_4.setAutoExclusive(1)
         self.Op1.setWordWrap(True)
         self.Op2.setWordWrap(True)
         self.Op3.setWordWrap(True)
         self.Op4.setWordWrap(True)
         self.Op1.setText(op1)
         self.Op2.setText(op2)
         self.Op3.setText(op3)
         self.Op4.setText(op4)
         self.scoreA.display(scrB)
      except:
         self.hide()
         self.final_result()

   def anscheckB_pres(self):
      print "anscheck_B"
      
      global present_ans,scrB,q_id,presentusr_q,presentans_list,present_recno,q_list,present_q,present_cnt,txtbwsr,year,scrA,q_cnt
      print q_cnt
      if timestrB==0 or q_cnt==29:
         return
      print txtbwsr
      if self.Opt_1.isChecked()==0 and self.Opt_2.isChecked()==0 and self.Opt_3.isChecked()==0 and self.Opt_4.isChecked()==0:
         return
         
      q_cnt+=1
      option=str(0)
      
      for radioButton in self.findChildren(QtGui.QRadioButton):
         if radioButton.isChecked():
            radioButtonText = str(radioButton.text())
            option = radioButtonText.strip()[0:1]
            #print option
            if option == present_ans:
               scrB = scrB+4
               correct=1
               self.scoreA.display(scrB)
            else:
               scrB = scrB-2
               correct=0
               self.scoreA.display(scrB)
               
      if q_cnt ==29:
         self.final_result()         

      presentusr_q+=(str(q_id))
      presentusr_q+=('@')
     #print presentusr_q
      pq_list.append(q_id)
      #print pq_list
      #print "anscheckB_pres"
               
      presentans_list+=(option)
      presentans_list+=('@')
     #print presentans_list
      listcount=0
      
      #give a unique randon index for present_q  
      del present_q[present_recno]
      present_cnt=len(present_q)
      present_recno = random.randint(0, (present_cnt))
      #print present_q
      try:
          ansbox = self.findChild(QtGui.QTextBrowser, "ansbox_"+str(txtbwsr))

          if correct==1:
            year+=1
            ansbox.setStyleSheet(_fromUtf8("background-color : rgb(15,85,71)"))
          else:
            year-=1
            ansbox.setStyleSheet(_fromUtf8("background-color : rgb(157,48,48)"))
          #ansbox.append(str(year))
          ansbox.append("<font color = white ><font size = 4> %s </font>" %  (str(year)) )

          txtbwsr -=1
          print txtbwsr
          self.showqueB_pres()
      except:
          self.final_result()

   def restartC(self):
     #print "restartC"
      global rcptno,timestrB,scrB,pq_list,presentusr_q,presentans_list,present_recno,scrA
      resq_list=[]
      sql = "SELECT Score_A FROM UserMcqDB WHERE R_No ="+rcptno
      res = conn.execute(str(sql))
      resc = res.fetchone()
      scrA = int(resc[0])      
      sqlstr1 = "SELECT R_No, Q_List,Timer_B,Score_B,Ans_B FROM Part2_DB WHERE R_No = "+rcptno
      rescur= conn.execute(str(sqlstr1))
      row = rescur.fetchone()
     #print row
      res_q = str(row[1])
      res_time = row[2]
      res_scr = row[3]
      res_ans = str(row[4])
      resq_list = res_q.split('@')
      #del resq_list[0]
      del resq_list[-1]
      #print resq_list
      timestrB = res_time
      presentusr_q=str(res_q)
      scrB=res_scr
      presentans_list = str(res_ans)
      q_list = resq_list
     #print q_list
      self.present_createlist()
      

    

#----------------------------PAST---------------------------------------------------


   def past_mcq(self):
      global past_cnt,timestrB,pastusr_q,pastans_list,past_q,past_recno,q_id,resp_list,rcptno,txtbwsr,p
      if p>"B":
         return
     #print "past_mcq"
      #self.formres.hide()
      #self.uires.past_btn.setEnabled(False)
      #self.uires.present_btn.setEnabled(False)
      #self.uires.future_btn.setEnabled(False)
      
      p="B"
      print p
      #past_cnt=0
      QtGui.QMainWindow.__init__(self)
      self.setupUi(self)
      self.showFullScreen()
      self.skipbutton.setEnabled(False)
      conn.execute(str("UPDATE FlagDB SET Part = 'B' WHERE R_No = "+rcptno+""))
      conn.commit()
      txtbwsr=30
      self.showqueB()
      self.nextbutton.clicked.connect(self.anscheckB)
      

      self.timerA.display(timestrB)
      self.timer = QTimer(self)
      self.timer.timeout.connect(self.TimerTickB)
      self.timer.start(1000)

   #TimerTick function to display countdown timer
   def TimerTickB(self):
      #print "timerB"
      global timestrB,timeflag,rcptno,pastusr_q,pastans_list,scrB
      if timestrB==0:
         #timeflagB_p=1
         self.timer.stop()
         self.final_result()
      else:
         timestrB -= 1
         self.timerA.display(timestrB)
         if ((timestrB%5)==0):
            sqlstr1 = "INSERT OR IGNORE INTO Part2_DB (R_No, Q_List,Timer_B,Score_B,Ans_B) VALUES("+ rcptno+",'"+ pastusr_q+"'," + str(timestrB) +"," + str(scrB) +",'" +  pastans_list + "')"
            conn.execute(str(sqlstr1))
            conn.commit()
            sqlstr2 = "UPDATE Part2_DB SET R_No="+ rcptno+", Q_List='"+ pastusr_q+"',Timer_B=" + str(timestrB) +",Score_B=" + str(scrB) +",Ans_B='" +  pastans_list + "' WHERE R_No="+ rcptno+" "
            conn.execute(str(sqlstr2))
            conn.commit()
            
   def showqueB(self):
     #print "showqueB"
      global past_cnt , past_recno, past_ans,tablename,q_id
      if (past_recno < 0) :
         past_recno = 0
      if (past_recno >= past_cnt) :
        #print past_recno, past_cnt
         past_recno = past_cnt-1
         
      #print past_q[past_recno]
      try:
         pastcur = conn.execute("SELECT ques, optA, optB, optC, optD, correctOpt  from '"+tablename+"' WHERE ques_id="+str(past_q[past_recno])+"")
         row = pastcur.fetchone()
         q_id = past_q[past_recno]
        #print q_id
         q= row[0]
         op1= row[1]
         op2= row[2]
         op3= row[3]
         op4= row[4]
         past_ans = row[5]
         #print past_ans
         self.Question.clear()
         self.Question.append(q)
         self.Question.update()
         self.Opt_1.isChecked()==0
         self.Opt_2.isChecked()==0
         self.Opt_3.isChecked()==0
         self.Opt_4.isChecked()==0
         self.Opt_1.setAutoExclusive(0)
         self.Opt_1.setChecked(False)
         self.Opt_2.setAutoExclusive(0)
         self.Opt_2.setChecked(False)
         self.Opt_3.setAutoExclusive(0)
         self.Opt_3.setChecked(False)
         self.Opt_4.setAutoExclusive(0)
         self.Opt_4.setChecked(False)
         self.Opt_1.setAutoExclusive(1)
         self.Opt_2.setAutoExclusive(1)
         self.Opt_3.setAutoExclusive(1)
         self.Opt_4.setAutoExclusive(1)
         self.Op1.setWordWrap(True)
         self.Op2.setWordWrap(True)
         self.Op3.setWordWrap(True)
         self.Op4.setWordWrap(True)
         self.Op1.setText(op1)
         self.Op2.setText(op2)
         self.Op3.setText(op3)
         self.Op4.setText(op4)
         self.scoreA.display(scrB)
      except:
         self.hide()
         self.final_result()
      
   def anscheckB(self):
     #print "anscheckB"
      global past_ans,scrB,q_id,pastusr_q,pastans_list,past_recno,q_list,past_q,past_cnt,txtbwsr,year
      if self.Opt_1.isChecked()==0 and self.Opt_2.isChecked()==0 and self.Opt_3.isChecked()==0 and self.Opt_4.isChecked()==0:
         return
      option=str(0)
      for radioButton in self.findChildren(QtGui.QRadioButton):
         if radioButton.isChecked():
            radioButtonText = str(radioButton.text())
            option = radioButtonText.strip()[0:1]
            #print option
            if option == past_ans:
               scrB = scrB+4
               correct=1
               #past_q+='1'
               #past_q+='@'
               self.scoreA.display(scrB)
            else:
               scrB = scrB-4
               correct=0
               self.scoreA.display(scrB)
               #past_cnt+=1
               #past_q.append(q_id)
               

      pastusr_q+=(str(q_id))
      pastusr_q+=('@')
     #print pastusr_q
               
      pastans_list+=(option)
      pastans_list+=('@')
      #print ans_list
      
      del past_q[past_recno]
      past_cnt=len(past_q)
      past_recno = random.randint(0, (past_cnt))
     #print past_q

      ansbox = self.findChild(QtGui.QTextBrowser, "ansbox_"+str(txtbwsr))
      
      if correct==1:
      	year+=1
      	ansbox.setStyleSheet(_fromUtf8("background-color : rgb(15,85,71)"))
      else:
        year-=1
        ansbox.setStyleSheet(_fromUtf8("background-color : rgb(157,48,48)"))
        #ansbox.append(str(year))

      ansbox.append("<font color = white ><font size = 4> %s </font>" %  (str(year)) )

      txtbwsr -=1
      
      self.showqueB()


   def restartB(self):
      print "restartB"
      #self.uires.hide()
      global rcptno,timestrB,scrB,past_q,pastusr_q,pastans_list,past_recno,past_cnt,scrA
      resq_list=[]
      sql = "SELECT Score_A FROM UserMcqDB WHERE R_No ="+rcptno
      res = conn.execute(str(sql))
      resc = res.fetchone()
      scrA = int(resc[0])
      sqlstr1 = "SELECT R_No, Q_List,Timer_B,Score_B,Ans_B FROM Part2_DB WHERE R_No = "+rcptno
      rescur= conn.execute(str(sqlstr1))
      row = rescur.fetchone()
      #print row
      sqlstr2 = "SELECT R_No , Q_List FROM FlagDB WHERE R_No = "+rcptno
      q_cur = conn.execute(str(sqlstr2))
      res = q_cur.fetchone()
     #print res
      
      respast_q = str(res[1])
      past_q = respast_q.split('@')
      del past_q[-1]
     #print past_q
      past_cnt = len(past_q)
      user_resq = str(row[1])
      res_time = row[2]
      res_scr = row[3]
      res_ans = str(row[4])
      resq_list = user_resq.split('@')

      #del resq_list[0]
      del resq_list[-1]
      #del resq_list[-2]
      #print resq_list
      for ele in past_q:
          if ele in resq_list:
              past_q.remove(ele)

     #print past_q
      timestrB = res_time
      pastusr_q=str(user_resq)
      scrB=res_scr
      pastans_list = str(res_ans)
      #self.randit()
      self.past_mcq()



#------------------------------------------------------FUTURE------------------------------------------------------------------



      
   def future(self):
      global rcptno,timestrB,f_ans,f_id,f_recno,f_count,fq_list,f_anslist,p
      if p=="B" or p=="C":
         return
      p="D"
      print p
      #self.formres.hide()
      #self.uires.past_btn.setEnabled(False)
      #self.uires.present_btn.setEnabled(False)
      #self.uires.future_btn.setEnabled(False)
      #self.skipbutton.setEnabled(False)
      #self.nextbutton.setEnabled(False)
      
      self.eulerform=QtGui.QMainWindow()
      self.partB=euler.Ui_MainWindow()
      self.partB.setupUi(self.eulerform)
      self.eulerform.showFullScreen()
      conn.execute(str("UPDATE FlagDB SET Part = 'D' WHERE R_No = "+rcptno+""))
      conn.commit()
      

      self.showfuture()
      self.partB.submit_B.clicked.connect(self.f_anscheck)
      self.partB.next_B.clicked.connect(self.f_skip)

      self.partB.timerB.display(timestrB)
      self.timer = QTimer(self)
      self.timer.timeout.connect(self.TimerTickF)
      self.timer.start(1000)


   def f_skip(self):
      global f_skipcnt
      #self.f_skipcount.display(f_skipcnt)
      if f_skipcnt==0:
         QMessageBox.about(self,'Clash','Out of skips')
         self.partB.next_B.setEnabled(False)
         return
      else:
         f_skipcnt-=1
         self.partB.f_skipcount.display(f_skipcnt)
         self.f_next()

         
   def showfuture(self):
      global timestrB,f_ans,f_id,f_recno,f_count,fq_list,f_skipcnt
      try:
         fcursor = conn.execute("SELECT Q_ID, Question,Correct_Ans  from EulerQuestionDB limit " + str(f_recno) + ",1")
         row = fcursor.fetchone()
         f_id=f_recno
         q=row[1]
         f_ans=row[2]
         #print f_ans
         self.partB.Question_B.clear()
         self.partB.Question_B.append(q)
         self.partB.Question_B.update()
         self.partB.f_skipcount.display(f_skipcnt)
         fq_list.append(f_id)
         self.partB.scoreB.display(scrB)
      except:
         self.eulerform.hide()
         self.final_result()
      

   #TimerTick function to display countdown timer
   def TimerTickF(self):
      global timestrB,timeflag,f_anslist,scrB,rcptno,fq
      print timestrB
      if timestrB==0:
         self.timer.stop()
         self.eulerform.hide()
         self.final_result()
      else:
         timestrB-=1
         self.partB.timerB.display(timestrB)
         if ((timestrB%5)==0):
            sqlstr1 = "INSERT OR IGNORE INTO Part2_DB (R_No, Q_List,Timer_B,Score_B,Ans_B) VALUES("+ rcptno+",'"+ fq+"'," + str(timestrB) +"," + str(scrB) +",'" +  f_anslist + "')"
            conn.execute(str(sqlstr1))
            conn.commit()
            sqlstr2 = "UPDATE Part2_DB SET R_No="+ rcptno+", Q_List='"+ fq+"',Timer_B=" + str(timestrB) +",Score_B=" + str(scrB) +",Ans_B='" +  f_anslist + "' WHERE R_No="+ rcptno+" "
            conn.execute(str(sqlstr2))
            conn.commit()




   def f_anscheck(self):
      print "f_check"
      global f_ans,f_id,scrB,fq_list,rcptno,fq,f_anslist
      
      fq+=str(f_id)
      fq+='@'
      usr_ans=self.partB.Ans_B.text()
      self.partB.Ans_B.clear()
     #print usr_ans
      usr_ans = str(usr_ans)
      f_anslist+=str(usr_ans)
      f_anslist+='@'
      f_ans = str(f_ans)
      f_ans.replace(" ","")
      usr_ans.replace(" ","")
      
     #print usr_ans
     #print f_ans
      if str(f_ans) == str(usr_ans):
         scrB = scrB +5
         self.partB.scoreB.display(scrB)
         self.f_next()
      else:
         QMessageBox.about(self,'Clash','Wrong answer! You may Try again!')

   def f_next(self):
      global f_recno,f_count,fq_list
      f_recno = random.randint(0, (f_count))
      #print f_recno
      flg1 = (f_recno) in fq_list
      #if flg1 :
         #print "exists " , f_recno
      excnt = 0 
      while flg1 and (excnt < f_count):
         f_recno = random.randint(0, (f_count))
         flg1 = (f_recno) in fq_list
         excnt += 1
        #print excnt , "---", f_recno
      self.showfuture()         


   def restartD(self):
      global f_recno,f_count,fq,f_anslist,timestrB,scrB,rcptno,fq_list,scrA
      sql = "SELECT Score_A FROM UserMcqDB WHERE R_No ="+rcptno
      res = conn.execute(str(sql))
      resc = res.fetchone()
      scrA = int(resc[0])
      sqlstr1 = "SELECT R_No, Q_List,Timer_B,Score_B,Ans_B FROM Part2_DB WHERE R_No = "+rcptno
      rescur= conn.execute(str(sqlstr1))
      row = rescur.fetchone()
     #print row
      resq_list= []
      resq_list = str(row[1])
      fq_list = resq_list.split('@')
      del fq_list[-1]
     #print fq_list
      fq = resq_list
      res_time = row[2]
      res_scr = row[3]
      res_ans = str(row[4])
      timestrB = res_time
      scrB = res_scr
      f_anslist = res_ans
      for q in fq_list:
          if q in fq_list:
              fq_list.remove(q)

      self.future()
      self.f_next()







      
   def final_result(self):
     global scrA,scrB,rcptno,nm1,nm2,colgname,rnd
     
     #self.uires.past_btn.setEnabled(False)
     #self.uires.present_btn.setEnabled(False)
     #self.uires.future_btn.setEnabled(False)
     #self.skipbutton.setEnabled(False)
     #self.nextbutton.setEnabled(False)
     #self.ui.loginbutton.setEnabled(False)
     totalscr=scrA+scrB
     self.timer.stop()
     conn.execute("UPDATE ServerDB SET Score_A= ?,Score_B= ?,Total_Score= ? WHERE R_No= ?",(scrA,scrB,totalscr,int(rcptno)))
     conn.commit()
      
      #sending http post

     
     self.finalresform=QtGui.QMainWindow()
     self.finalres=Final_result.Ui_MainWindow()
     self.finalres.setupUi(self.finalresform)
     self.finalres.scoreA.display(scrA)
     self.finalres.scoreB.display(scrB)  
     self.finalres.total_scr.display(scrA+scrB)
     self.finalresform.showFullScreen()
     poststr="http://clash14.pythonanywhere.com/tomjerrypopeyeolive/"+str(rcptno)+"@"+nm1+"@"+nm2+"@"+colgname+"@"+str(scrA)+"@"+str(scrB)+"@"+str(totalscr)+"@"+rnd
     print poststr
   
   
     

if __name__ == '__main__':

   import sys
   app = QtGui.QApplication(sys.argv)
   window = Window()
   sys.exit(app.exec_())
