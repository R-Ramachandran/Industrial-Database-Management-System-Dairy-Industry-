# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import MySQLdb
import re

class Ui_LoginPage(object):

    def login(self):
        from AdminPage1 import Ui_AdminPage1
        from EmployeePage1 import Ui_EmployeePage1
        from SellerPage1 import Ui_SellerPage1
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        username=self.lineEdit.text()
        password=self.lineEdit_2.text()
        c.execute("select count(user_id) from login where user_id = %s",[username])
        check=list(c)[0][0]
        if check>0:
            c.execute("select * from login where user_id = %s and password = %s",[username,password])
            result=list(map(list,c))
            if len(result)>0 and len(re.findall("admin$",result[0][0]))==1 and password==result[0][1]:
                c.close()
                db.close()
                self.AdP1 = QtWidgets.QMainWindow()
                self.ui = Ui_AdminPage1(self.lineEdit.text(),self.lineEdit_2.text())
                self.ui.setupUi(self.AdP1)
                self.LoginPage.hide()
                self.AdP1.show()
            elif len(result)>0 and len(re.findall("employee$",result[0][0]))==1 and password==result[0][1]:
                c.close()
                db.close()
                self.EmP1 = QtWidgets.QMainWindow()
                self.ui = Ui_EmployeePage1(self.lineEdit.text(),self.lineEdit_2.text())
                self.ui.setupUi(self.EmP1)
                self.LoginPage.hide()
                self.EmP1.show()
            elif len(result)>0 and len(re.findall("seller$",result[0][0]))==1 and password==result[0][1]:
                c.close()
                db.close()
                self.SeP1 = QtWidgets.QMainWindow()
                self.ui = Ui_SellerPage1(self.lineEdit.text(),self.lineEdit_2.text())
                self.ui.setupUi(self.SeP1)
                self.LoginPage.hide()
                self.SeP1.show() 
            else:
                QtWidgets.QMessageBox.warning(self.lineEdit, 'Error','Check your User ID and Password 😊')
        elif username=="" or password=="":
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','User ID or Password Cannot be Empty')
        else:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','User ID doesnot Exist!!!')
    def openAdminSignUp(self):
        from AdminSignUp import Ui_AdminSignUp                                      
        self.ASU = QtWidgets.QMainWindow()
        self.ui = Ui_AdminSignUp()
        self.ui.setupUi(self.ASU)
        self.LoginPage.hide()
        self.ASU.show()    
    def openEmployeeSignUp(self):
        from EmployeeSignUp import Ui_EmployeeSignUp
        self.ESU = QtWidgets.QMainWindow()
        self.ui = Ui_EmployeeSignUp()
        self.ui.setupUi(self.ESU)
        self.LoginPage.hide()
        self.ESU.show()
    def openSellerSignUp(self):
        from SellerSignUp import Ui_SellerSignUp
        self.SSU = QtWidgets.QMainWindow()
        self.ui = Ui_SellerSignUp()
        self.ui.setupUi(self.SSU)
        self.LoginPage.hide()
        self.SSU.show()
    def setupUi(self, LoginPage):
        self.LoginPage=LoginPage
        LoginPage.setObjectName("LoginPage")
        #LoginPage.resize(1046, 707)                    # Make a Note of it
        LoginPage.setFixedSize(1046, 707)               # Make a Note of it
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Logo/Images/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LoginPage.setWindowIcon(icon)
        LoginPage.setWindowFlags(LoginPage.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint) # Make a Note of it
        LoginPage.setAutoFillBackground(False)
        LoginPage.setStyleSheet("background-color: rgb(0, 170, 255);")
        LoginPage.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(LoginPage)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 30, 1001, 61))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setMouseTracking(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 180, 591, 341))
        self.label_2.setPixmap(QtGui.QPixmap(":/Cow/LoginCow.jpg"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(620, 180, 401, 431))
        self.frame.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(90, 280, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 350, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(181, 181, 181);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.openAdminSignUp)          # Make a Note of it
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.LoginPage.lineEdit = self.lineEdit
        self.lineEdit.setGeometry(QtCore.QRect(180, 20, 211, 41))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)                # Make a Note of it
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(10, 90, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(150, 150, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(181, 181, 181);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.login)        # Make a Note of it
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(180, 90, 211, 41))
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)   # Make a Note of it
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)         # Make a Note of it
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(280, 350, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background-color: rgb(181, 181, 181);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.openSellerSignUp)          # Make a Note of it
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(140, 350, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("background-color: rgb(181, 181, 181);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.openEmployeeSignUp)        # Make a Note of it
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setGeometry(QtCore.QRect(0, 200, 401, 16))
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(3)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setGeometry(QtCore.QRect(0, 240, 401, 16))
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(3)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(170, 210, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.frame.raise_()
        self.label.raise_()
        self.label_2.raise_()
        LoginPage.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(LoginPage)
        self.statusbar.setObjectName("statusbar")
        LoginPage.setStatusBar(self.statusbar)

        self.retranslateUi(LoginPage)
        QtCore.QMetaObject.connectSlotsByName(LoginPage)

    def retranslateUi(self, LoginPage):
        _translate = QtCore.QCoreApplication.translate
        LoginPage.setWindowTitle(_translate("LoginPage", "Welcome"))
        self.label.setText(_translate("LoginPage", "<html><head/><body><p><span style=\" color:#55007f;\">DAIRY INDUSTRY DATABASE MANAGEMENT SYSTEM</span></p></body></html>"))
        self.label_2.setText(_translate("LoginPage", "<html><head/><body><p><img src=\":/Cow/Images/LoginCow.jpg\"/></p></body></html>"))
        self.label_5.setText(_translate("LoginPage", " NEW USER ? SIGNUP AS"))
        self.pushButton_2.setText(_translate("LoginPage", "ADMIN"))
        self.label_3.setText(_translate("LoginPage", "USERNAME"))
        self.label_4.setText(_translate("LoginPage", "PASSWORD"))
        self.pushButton.setText(_translate("LoginPage", "LOGIN"))
        self.pushButton_3.setText(_translate("LoginPage", "SELLER"))
        self.pushButton_4.setText(_translate("LoginPage", "EMPLOYEE"))
        self.label_6.setText(_translate("LoginPage", " OR"))

import LoginCowR
import LogoR

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoginPage = QtWidgets.QMainWindow()
    ui = Ui_LoginPage()
    ui.setupUi(LoginPage)
    LoginPage.show()
    sys.exit(app.exec_())

