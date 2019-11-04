# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import MySQLdb
import re

class Ui_EmployeeConfirmation(object):

    def __init__( self, userid, password, l1, flag):                                           # Make a Note of it
        self.userid=userid
        self.password=password
        self.l1 = l1
        self.flag = flag
    
    def logout(self):
        self.EmployeeConfirmation.close()

    def saveEmployee(self):
        from AdminPage1 import Ui_AdminPage1
        self.LP = QtWidgets.QMainWindow()
        self.ui = Ui_AdminPage1(self.userid,self.password)
        self.ui = Ui_AdminPage1(self.userid,self.password)
        self.ui.setupUi(self.LP)
        for i in range(len(self.l1)):
            self.l1[i]=list(self.l1[i])
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        flag1 = 1
        l3 = []
        l4 = []
        if self.flag == 1 and flag1 == 1:
            c.execute("select e_id, e_name, e_user_id, e_dob, e_ph, e_d_id, e_job_title, e_join_date, e_salary from employee")
            l2 = c.fetchall()
            for i in range(len(l2)):
                l3.append(l2[i][0])
            for i in range(len(self.l1)):
                l4.append(self.l1[i][0])
            for i in range(len(l2)):
                if l3[i] not in l4:
                    c.execute("select e_id, e_name, e_user_id, e_dob, e_ph, e_d_id, e_job_title, e_join_date, e_salary from employee where e_id = %s",[self.lineEdit.text()])
                    res1 = c.fetchall()
                    c.execute("select d_a_id from department where d_a_id = %s and d_name = %s",[self.ui.id,l2[i][5]])
                    res = c.fetchall()
                    print(res,res1)
                    if len(res1) !=0 and len(res) !=0:
                        c.execute("delete from employee where e_id = %s",[l2[i][0]])
                        c.execute("update bill set b_e_id = %s where b_e_id = %s",[self.lineEdit.text(),l2[i][0]])
                        c.execute("delete from login where user_id = %s",[l2[i][2]])
                        c.execute("update seller set s_e_id = %s where s_e_id = %s",[self.lineEdit.text(),l2[i][0]])
                        c.execute("commit")
                    elif len(res1)==0 and len(res)!=0:
                        QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Employee ID doesnot Exist')
                    else:
                        QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry!!! You cannot Delete Employee in Other Department')
        elif self.flag==0 and flag1==1:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Check Entered Values and Cell cannot be Empty')
        elif self.flag==1 and flag1==0:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! You have already Entered the Cattle Type in Todays Sale, Try to modify the respective Milk Quantity')
        else:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Check Entered Values and Cell cannot be Empty. Also, You have already Entered the Cattle Type in Todays Sale, Try to modify the respective Milk Quantity')



    def setupUi(self, EmployeeConfirmation):
        EmployeeConfirmation.setObjectName("EmployeeConfirmation")
        self.EmployeeConfirmation = EmployeeConfirmation
        EmployeeConfirmation.resize(616, 210)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Logo/Images/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        EmployeeConfirmation.setWindowIcon(icon)
        EmployeeConfirmation.setStyleSheet("background-color: rgb(255, 85, 0);")
        EmployeeConfirmation.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(EmployeeConfirmation)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 611, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 0, 127);")
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 611, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(0, 0, 127);")
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 611, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(0, 0, 127);")
        self.label_3.setScaledContents(True)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 50, 611, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(0, 0, 127);")
        self.label_4.setScaledContents(True)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(100, 161, 174, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color: rgb(0, 255, 0);\n"
"color: rgb(170, 0, 255);")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(282, 160, 171, 35))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(460, 160, 51, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(0, 255, 255);")
        self.pushButton.clicked.connect(self.saveEmployee)
        self.pushButton.setObjectName("pushButton")
        EmployeeConfirmation.setCentralWidget(self.centralwidget)

        self.retranslateUi(EmployeeConfirmation)
        QtCore.QMetaObject.connectSlotsByName(EmployeeConfirmation)

    def retranslateUi(self, EmployeeConfirmation):
        _translate = QtCore.QCoreApplication.translate
        EmployeeConfirmation.setWindowTitle(_translate("EmployeeConfirmation", "Confirmation"))
        self.label.setText(_translate("EmployeeConfirmation", "Are you sure to Remove the Employee ? If you Delete "))
        self.label_2.setText(_translate("EmployeeConfirmation", "Employee to some other Employee, So please Enter the"))
        self.label_3.setText(_translate("EmployeeConfirmation", "Employee ID to be Assigned in Purchase Department :"))
        self.label_4.setText(_translate("EmployeeConfirmation", "the Employee, you want to Assign Sellers under that"))
        self.label_5.setText(_translate("EmployeeConfirmation", "Employee ID :"))
        self.pushButton.setText(_translate("EmployeeConfirmation", "Ok"))

import LogoR