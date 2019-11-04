# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import MySQLdb
import re
from datetime import date

class Ui_SellerSignUp(object):

    def submit(self):
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        name = self.lineEdit.text()
        seller_id = self.lineEdit_2.text()
        ph_no = self.lineEdit_3.text()
        address = self.lineEdit_5.text()
        dob = self.lineEdit_4.text()
        gender = self.lineEdit_7.text()
        employee_id = self.lineEdit_13.text()
        salary = self.lineEdit_12.text()
        user_id = self.lineEdit_9.text()
        password = self.lineEdit_10.text()
        re_password = self.lineEdit_11.text()
        imagePath = "D:/VIT/Database Management System/Project/PyQT/Images/Admin.png"
        if ph_no[0]!='0' and len(ph_no)==10:
            check=1
        else:
            check=0

        if re.match("^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$",dob):
            year=int(dob[-4:])
            this_year=int(date.today().strftime("%d/%m/%Y")[-4:])
            check1=1
        else:
            check1=0

        c.execute("select D_A_Id from department where D_Name = %s",["Purchase"])
        if len(c.fetchall())==0:
            insert=1
        else:
            insert=0

        c.execute("select E_Id from employee where E_Id = %s and E_D_ID = %s",[employee_id,"Purchase"])
        if len(c.fetchall())==0:
            insert1=1
        else:
            insert1=0
        if password==re_password and password=="":
            QtWidgets.QMessageBox.information(self.lineEdit_10, 'Error','Sorry, Please Enter The Password')
        elif password!=re_password:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry, Entered Password and Re-Entered Password Doesnot Match')
        elif (name=="") or (employee_id=="") or (ph_no=="") or (user_id=="") or (dob=="") or (seller_id=="") or (salary==""):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Name, ID, Phone No., User ID, DOB and Salary cannot be Empty')
        elif check1!=1 and dob!="":
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Check Date format(should be dd/mm/yyyy)')
        elif insert==1:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Entered Department doesnot Exist')
        elif insert1==1:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Admin ID or Department doesnot Exist')
        elif (employee_id!="" and int(employee_id)<0) or (seller_id!="" and int(seller_id)<0):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! ID cannot be negative')
        elif (salary!="" and int(salary)<0):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Salary cannot be negative')
        elif (check1==1 and (this_year-year)<=18):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Your Not eligible to Register')
        elif check!=1:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Check your Phone Number')
        elif gender!="" and (gender not in ["M","m","F","f"]):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error',r'Sorry! Enter M/m for Male and F/f for Female')
        elif len(re.findall("seller$",user_id))==0:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! User ID should end with .seller')
        elif (len(seller_id)>15) or (len(user_id)>15) or (len(password)>15) or len(employee_id)>15 or (len(salary)>15):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Length of User ID, Admin ID, Employee ID, Password, Job Title and Department Name cannot be more than 15')
        elif (len(name)>40):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Length of Name cannot be more than 40')
        elif (len(address)>100):
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Length of Address cannot be more than 100')
        else:
            c.execute("select S_Id from seller")
            result = list(c)
            flag1=1
            for i in result:
                if seller_id==i[0]:
                    flag1=0
                    break
            c.execute("select S_User_Id from seller")
            result = list(c)
            flag2=1
            for i in result:
                if user_id==i[0]:
                    flag2=0
                    break
            if flag1==0 and flag2!=0:
                QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry, Seller ID Already Exist!!!')
            elif flag1!=0 and flag2==0:
                QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry, User ID Already Exist!!!')
            elif flag1==0 and flag2==0:
                QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry, User ID and Seller ID Already Exist!!!')
            else:
                c.execute("insert into seller values( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[name,seller_id,gender,dob,salary,employee_id,ph_no,address,user_id,password,imagePath])
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
        self.SellerSignUp.hide()
        self.LP.show()

    def setupUi(self, SellerSignUp):
        self.SellerSignUp=SellerSignUp
        SellerSignUp.setObjectName("SellerSignUp")
        #SellerSignUp.resize(1046, 707)                    # Make a Note of it
        SellerSignUp.setFixedSize(1046, 707)               # Make a Note of it
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Logo/Images/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SellerSignUp.setWindowIcon(icon)
        SellerSignUp.setWindowFlags(SellerSignUp.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint) # Make a Note of it
        SellerSignUp.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.centralwidget = QtWidgets.QWidget(SellerSignUp)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(150, 60, 741, 561))
        self.frame.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setGeometry(QtCore.QRect(10, 210, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.label_18 = QtWidgets.QLabel(self.frame)
        self.label_18.setGeometry(QtCore.QRect(10, 410, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setGeometry(QtCore.QRect(10, 160, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(10, 60, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_16 = QtWidgets.QLabel(self.frame)
        self.label_16.setGeometry(QtCore.QRect(10, 260, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(10, 110, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_20 = QtWidgets.QLabel(self.frame)
        self.label_20.setGeometry(QtCore.QRect(10, 460, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(370, 10, 361, 41))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(370, 60, 361, 41))
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
        self.lineEdit_3.setGeometry(QtCore.QRect(370, 110, 361, 41))
        self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_4.setGeometry(QtCore.QRect(370, 210, 361, 41))
        self.lineEdit_4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_5.setGeometry(QtCore.QRect(370, 160, 361, 41))
        self.lineEdit_5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_7.setGeometry(QtCore.QRect(370, 260, 361, 41))
        self.lineEdit_7.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_7.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_9.setGeometry(QtCore.QRect(370, 410, 361, 41))
        self.lineEdit_9.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_9.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_10.setGeometry(QtCore.QRect(370, 460, 361, 41))
        self.lineEdit_10.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_10.setEchoMode(QtWidgets.QLineEdit.Password)   # Make a Note of it
        self.lineEdit_10.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.label_21 = QtWidgets.QLabel(self.frame)
        self.label_21.setGeometry(QtCore.QRect(10, 510, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.lineEdit_11 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_11.setGeometry(QtCore.QRect(370, 510, 361, 41))
        self.lineEdit_11.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_11.setEchoMode(QtWidgets.QLineEdit.Password)   # Make a Note of it
        self.lineEdit_11.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.label_22 = QtWidgets.QLabel(self.frame)
        self.label_22.setGeometry(QtCore.QRect(10, 310, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName("label_22")
        self.lineEdit_12 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_12.setGeometry(QtCore.QRect(370, 310, 361, 41))
        self.lineEdit_12.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_12.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.lineEdit_13 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_13.setGeometry(QtCore.QRect(370, 360, 361, 41))
        self.lineEdit_13.setFont(font)
        self.lineEdit_13.setStyleSheet("background-color: rgb(159, 159, 159);")
        self.lineEdit_13.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.label_23 = QtWidgets.QLabel(self.frame)
        self.label_23.setGeometry(QtCore.QRect(10, 360, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(580, 640, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(139, 139, 139);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openLoginPage)               # Make a Note of it
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 640, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(139, 139, 139);")
        self.pushButton_2.clicked.connect(self.submit)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(450, 10, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(139, 0, 209);")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(860, 656, 171, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        SellerSignUp.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SellerSignUp)
        self.statusbar.setObjectName("statusbar")
        SellerSignUp.setStatusBar(self.statusbar)

        self.retranslateUi(SellerSignUp)
        QtCore.QMetaObject.connectSlotsByName(SellerSignUp)

    def retranslateUi(self, SellerSignUp):
        _translate = QtCore.QCoreApplication.translate
        SellerSignUp.setWindowTitle(_translate("SellerSignUp", "Sign Up"))
        self.label_10.setText(_translate("SellerSignUp", "DATE OF BIRTH*"))
        self.label_18.setText(_translate("SellerSignUp", "USER ID*"))
        self.label_2.setText(_translate("SellerSignUp", "NAME*"))
        self.label_8.setText(_translate("SellerSignUp", "ADDRESS"))
        self.label_4.setText(_translate("SellerSignUp", "SELLER ID*"))
        self.label_16.setText(_translate("SellerSignUp", "GENDER"))
        self.label_6.setText(_translate("SellerSignUp", "PH. NO.*"))
        self.label_20.setText(_translate("SellerSignUp", "PASSWORD*"))
        self.label_21.setText(_translate("SellerSignUp", "RE-ENTER PASSWORD*"))
        self.label_22.setText(_translate("SellerSignUp", "SALARY*"))
        self.label_23.setText(_translate("SellerSignUp", "EMPLOYEE ID*"))
        self.pushButton.setText(_translate("SellerSignUp", "BACK"))
        self.pushButton_2.setText(_translate("SellerSignUp", "SUBMIT"))
        self.label.setText(_translate("SellerSignUp", "SIGN UP"))
        self.label_3.setText(_translate("SellerSignUp", "*MUST BE FILLED"))

import LogoR

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SellerSignUp = QtWidgets.QMainWindow()
    ui = Ui_SellerSignUp()
    ui.setupUi(SellerSignUp)
    SellerSignUp.show()
    sys.exit(app.exec_())

