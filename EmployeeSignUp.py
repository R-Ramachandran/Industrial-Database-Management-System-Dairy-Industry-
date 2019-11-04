# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import MySQLdb
import re
from datetime import date

class Ui_EmployeeSignUp(object):

    def submit(self):
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        name = self.lineEdit.text()
        employee_id = self.lineEdit_2.text()
        ph_no = self.lineEdit_3.text()
        address = self.lineEdit_5.text()
        dob = self.lineEdit_4.text()
        gender = self.lineEdit_7.text()
        department = self.lineEdit_8.text()
        job_title = self.lineEdit_9.text()
        admin_id = self.lineEdit_10.text()
        salary = self.lineEdit_11.text()
        user_id = self.lineEdit_17.text()
        password = self.lineEdit_18.text()
        re_password = self.lineEdit_19.text()
        doj = self.lineEdit_6.text()
        imagePath = "D:/VIT/Database Management System/Project/PyQT/Images/Admin.png"
        if ph_no[0]!='0' and len(ph_no)==10:
            check=1
        else:
            check=0

        if re.match("^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$",dob) and re.match("^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$",doj):
            year=int(dob[-4:])
            this_year=int(date.today().strftime("%d/%m/%Y")[-4:])
            check1=1
            year1=int(doj[-4:])
            check2=1
        else:
            check1=0
            check2=0

        c.execute("select D_A_Id from department where D_Name = %s",[department])
        if len(c.fetchall())==0:
            insert=1
        else:
            insert=0

        c.execute("select A_Id from admin where A_Id = %s and A_D_ID = %s",[admin_id,department])
        if len(c.fetchall())==0:
            insert1=1
        else:
            insert1=0
        if password==re_password and password=="":
            QtWidgets.QMessageBox.information(self.lineEdit_10, 'Error','Sorry, Please Enter The Password')
        elif password!=re_password:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry, Entered Password and Re-Entered Password Doesnot Match')
        elif (name=="") or (admin_id=="") or (ph_no=="") or (user_id=="") or (dob=="") or (department=="") or (employee_id=="") or (doj=="") or (salary=="") or (job_title==""):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Name, ID, Phone No., User ID, DOB, Department, Job Title, Salary and Date of Joining cannot be Empty')
        elif check1!=1 and dob!="":
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Check Date format(should be dd/mm/yyyy)')
        elif insert==1:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Entered Department doesnot Exist')
        elif insert1==1:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Admin ID or Department doesnot Exist')
        elif (admin_id!="" and int(admin_id)<0) or (employee_id!="" and int(employee_id)<0):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! ID cannot be negative')
        elif (salary!="" and int(salary)<0):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Salary cannot be negative')
        elif (check1==1 and (this_year-year)<=18):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Your Not eligible to Register')
        elif (check2==1 and (year1-year)<=18):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Check Your Join Date')
        elif check!=1:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Check your Phone Number')
        elif gender!="" and (gender not in ["M","m","F","f"]):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error',r'Sorry! Enter M/m for Male and F/f for Female')
        elif len(re.findall("employee$",user_id))==0:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! User ID should end with .employee')
        elif (len(admin_id)>15) or (len(department)>15) or (len(user_id)>15) or (len(password)>15) or len(employee_id)>15 or (len(job_title)>15) or (len(salary)>15):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Length of User ID, Admin ID, Employee ID, Password, Job Title and Department Name cannot be more than 15')
        elif (len(name)>40):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Length of Name cannot be more than 40')
        elif (len(address)>100):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Length of Address cannot be more than 100')
        else:
            c.execute("select E_Id from employee")
            result = list(c)
            flag1=1
            for i in result:
                if employee_id==i[0]:
                    flag1=0
                    break
            c.execute("select E_User_Id from employee")
            result = list(c)
            flag2=1
            for i in result:
                if user_id==i[0]:
                    flag2=0
                    break
            if flag1==0 and flag2!=0:
                QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry, Employee ID Already Exist!!!')
            elif flag1!=0 and flag2==0:
                QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry, User ID Already Exist!!!')
            elif flag1==0 and flag2==0:
                QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry, User ID and Employee ID Already Exist!!!')
            else:
                c.execute("insert into employee values( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[name,employee_id,gender,dob,department,admin_id,ph_no,salary,doj,address,job_title,user_id,password,imagePath])
                c.execute("insert into login values( %s, %s)",[user_id,password])
                c.execute("commit")
                c.close()
                db.close()
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("You have Successfully Signed Up!!!")
                msg.buttonClicked.connect(self.openLoginPage)
                msg.exec_()

    def openLoginPage(self):
        from LoginPage import Ui_LoginPage
        self.LP = QtWidgets.QMainWindow()
        self.ui = Ui_LoginPage()
        self.ui.setupUi(self.LP)
        self.EmployeeSignUp.hide()
        self.LP.show()

    def setupUi(self, EmployeeSignUp):
        self.EmployeeSignUp=EmployeeSignUp
        EmployeeSignUp.setObjectName("EmployeeSignUp")
        #EmployeeSignUp.resize(1046, 707)                    # Make a Note of it
        EmployeeSignUp.setFixedSize(1046, 707)               # Make a Note of it
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Logo/Images/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        EmployeeSignUp.setWindowIcon(icon)
        EmployeeSignUp.setWindowFlags(EmployeeSignUp.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint) # Make a Note of it
        EmployeeSignUp.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.centralwidget = QtWidgets.QWidget(EmployeeSignUp)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(620, 610, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(139, 139, 139);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openLoginPage)               # Make a Note of it
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(450, 40, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(139, 0, 209);")
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(320, 610, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.clicked.connect(self.submit)
        self.pushButton_2.setStyleSheet("background-color: rgb(139, 139, 139);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 130, 511, 421))
        self.frame.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setGeometry(QtCore.QRect(10, 190, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(10, 90, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_16 = QtWidgets.QLabel(self.frame)
        self.label_16.setGeometry(QtCore.QRect(10, 240, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(10, 140, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(220, 40, 281, 41))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(220, 90, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color: rgb(159, 159, 159);")
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_3.setGeometry(QtCore.QRect(220, 140, 281, 41))
        self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_4.setGeometry(QtCore.QRect(220, 190, 281, 41))
        self.lineEdit_4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_7.setGeometry(QtCore.QRect(220, 240, 281, 41))
        self.lineEdit_7.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_7.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setGeometry(QtCore.QRect(10, 340, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_5.setGeometry(QtCore.QRect(220, 340, 281, 41))
        self.lineEdit_5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(10, 290, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_6.setGeometry(QtCore.QRect(220, 290, 281, 41))
        self.lineEdit_6.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_6.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(530, 130, 511, 421))
        self.frame_2.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_22 = QtWidgets.QLabel(self.frame_2)
        self.label_22.setGeometry(QtCore.QRect(10, 240, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.frame_2)
        self.label_23.setGeometry(QtCore.QRect(10, 290, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.lineEdit_17 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_17.setGeometry(QtCore.QRect(220, 240, 281, 41))
        self.lineEdit_17.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_17.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.lineEdit_18 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_18.setGeometry(QtCore.QRect(220, 290, 281, 41))
        self.lineEdit_18.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_18.setEchoMode(QtWidgets.QLineEdit.Password)   # Make a Note of it
        self.lineEdit_18.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.label_24 = QtWidgets.QLabel(self.frame_2)
        self.label_24.setGeometry(QtCore.QRect(10, 340, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.label_24.setObjectName("label_24")
        self.lineEdit_19 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_19.setGeometry(QtCore.QRect(260, 340, 241, 41))
        self.lineEdit_19.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_19.setEchoMode(QtWidgets.QLineEdit.Password)   # Make a Note of it
        self.lineEdit_19.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.label_11 = QtWidgets.QLabel(self.frame_2)
        self.label_11.setGeometry(QtCore.QRect(10, 40, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.label_17 = QtWidgets.QLabel(self.frame_2)
        self.label_17.setGeometry(QtCore.QRect(10, 90, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.label_12 = QtWidgets.QLabel(self.frame_2)
        self.label_12.setGeometry(QtCore.QRect(10, 140, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_8.setGeometry(QtCore.QRect(220, 90, 281, 41))
        self.lineEdit_8.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_8.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_9.setGeometry(QtCore.QRect(220, 40, 281, 41))
        self.lineEdit_9.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_9.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.label_13 = QtWidgets.QLabel(self.frame_2)
        self.label_13.setGeometry(QtCore.QRect(10, 190, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_10.setGeometry(QtCore.QRect(220, 140, 281, 41))
        self.lineEdit_10.setFont(font)
        self.lineEdit_10.setStyleSheet("background-color: rgb(159, 159, 159);")
        self.lineEdit_10.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.lineEdit_11 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_11.setGeometry(QtCore.QRect(220, 190, 281, 41))
        self.lineEdit_11.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_11.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(840, 620, 171, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        EmployeeSignUp.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(EmployeeSignUp)
        self.statusbar.setObjectName("statusbar")
        EmployeeSignUp.setStatusBar(self.statusbar)

        self.retranslateUi(EmployeeSignUp)
        QtCore.QMetaObject.connectSlotsByName(EmployeeSignUp)

    def retranslateUi(self, EmployeeSignUp):
        _translate = QtCore.QCoreApplication.translate
        EmployeeSignUp.setWindowTitle(_translate("EmployeeSignUp", "Sign Up"))
        self.pushButton.setText(_translate("EmployeeSignUp", "BACK"))
        self.label.setText(_translate("EmployeeSignUp", "SIGN UP"))
        self.pushButton_2.setText(_translate("EmployeeSignUp", "SUBMIT"))
        self.label_10.setText(_translate("EmployeeSignUp", "DATE OF BIRTH*"))
        self.label_2.setText(_translate("EmployeeSignUp", "NAME*"))
        self.label_4.setText(_translate("EmployeeSignUp", "EMPLOYEE ID*"))
        self.label_16.setText(_translate("EmployeeSignUp", "GENDER"))
        self.label_6.setText(_translate("EmployeeSignUp", "PH. NO.*"))
        self.label_8.setText(_translate("EmployeeSignUp", "ADDRESS"))
        self.label_9.setText(_translate("EmployeeSignUp", "DATE OF JOINING*"))
        self.label_22.setText(_translate("EmployeeSignUp", "USER ID*"))
        self.label_23.setText(_translate("EmployeeSignUp", "PASSWORD*"))
        self.label_24.setText(_translate("EmployeeSignUp", "RE-ENTER PASSWORD*"))
        self.label_11.setText(_translate("EmployeeSignUp", "JOB TITLE*"))
        self.label_17.setText(_translate("EmployeeSignUp", "DEPARTMENT*"))
        self.label_12.setText(_translate("EmployeeSignUp", "ADMIN ID*"))
        self.label_13.setText(_translate("EmployeeSignUp", "SALARY*"))
        self.label_3.setText(_translate("EmployeeSignUp", "*MUST BE FILLED"))

import LogoR

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EmployeeSignUp = QtWidgets.QMainWindow()
    ui = Ui_EmployeeSignUp()
    ui.setupUi(EmployeeSignUp)
    EmployeeSignUp.show()
    sys.exit(app.exec_())

