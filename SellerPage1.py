# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import MySQLdb
from LoginPage import Ui_LoginPage
import re
from datetime import date

class Ui_SellerPage1(object):

    def __init__( self, userid, password):                                           # Make a Note of it
        self.userid=userid
        self.password=password
                
    def logout(self):
        self.LP = QtWidgets.QMainWindow()
        self.ui = Ui_LoginPage()
        self.ui.setupUi(self.LP)
        self.SellerPage1.close()
        self.LP.show()

    def saveProfile(self):
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        newName = self.lineEdit.text()
        newPh = self.lineEdit_6.text()
        newAddress = self.lineEdit_5.text()
        newDob = self.lineEdit_4.text()
        password = self.lineEdit_18.text()
        re_password = self.lineEdit_19.text()
        if ((newName==self.name) and (newPh==self.ph) and (newAddress==self.address) and (newDob==self.dob)) and ((password==self.password) or password==""):
            QtWidgets.QMessageBox.information(self.lineEdit_6, 'Pop-Up','Already Saved!!!')
        else:
            if newPh[0]!='0' and len(newPh)==10:
                check=1
            else:
                check=0
            if re.match("^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$",newDob):
                year=int(newDob[-4:])
                this_year=int(date.today().strftime("%d/%m/%Y")[-4:])
                check1=1
            else:
                check1=0
            if ((password!="" or re_password!="") and password!=re_password):
                QtWidgets.QMessageBox.information(self.lineEdit_18, 'Error','Sorry, Entered Password and Re-Entered Password Doesnot Match')
            elif (newName=="") or (newPh=="") or (newDob==""):
                QtWidgets.QMessageBox.information(self.lineEdit_6, 'Error','Sorry! Name, Phone No., DOB cannot be Empty')
            elif check1!=1 and newDob!="":
                QtWidgets.QMessageBox.information(self.lineEdit_4, 'Error','Sorry! Check Date format(should be dd/mm/yyyy)')
            elif check1==1 and (this_year-year)<=18:
                QtWidgets.QMessageBox.information(self.lineEdit_4, 'Error','Sorry! Check your Date Of Birth')
            elif check!=1:
                QtWidgets.QMessageBox.information(self.lineEdit_6, 'Error','Sorry! Check your Phone Number')
            elif (len(password)>15):
                QtWidgets.QMessageBox.information(self.lineEdit_18, 'Error','Sorry! Length of Password cannot be more than 15')
            elif (len(newName)>40):
                QtWidgets.QMessageBox.information(self.lineEdit_13, 'Error','Sorry! Length of Name cannot be more than 40')
            elif (len(newAddress)>100):
                QtWidgets.QMessageBox.information(self.lineEdit_5, 'Error','Sorry! Length of Address cannot be more than 100')
            else:
                if password=="" and re_password=="":
                    c.execute("update seller set s_name = %s, s_ph = %s, s_address = %s, s_dob = %s where s_user_id = %s",[newName,newPh,newAddress,newDob,self.userid])
                else:
                    self.password=password
                    c.execute("update seller set s_name = %s, s_ph = %s, s_address = %s, s_dob = %s, s_password = %s where s_user_id = %s",[newName,newPh,newAddress,newDob,password,self.userid])
                    c.execute("update login set password = %s where user_id = %s",[password,self.userid])
                c.execute("commit")    
                QtWidgets.QMessageBox.information(self.lineEdit_18, 'Pop-Up','Saved Successfully!!!')
                c.close()
                db.close()
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        c.execute("select * from seller where s_user_id = %s",[self.userid])
        result = c.fetchall()
        self.name = result[0][0]
        self.id = result[0][1]
        self.gender = result[0][2]
        self.dob = result[0][3]
        self.salary = result[0][4]
        self.employee_id = result[0][5]
        self.ph = result[0][6]
        self.address = result[0][7]
        c.close()
        db.close()
        self.lineEdit_18.setText("")
        self.lineEdit_19.setText("")

    def cancelProfile(self):
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        c.execute("select * from seller where s_user_id = %s",[self.userid])
        result = c.fetchall()
        self.name = result[0][0]
        self.ph = result[0][6]
        self.dob = result[0][3]
        self.address = result[0][7]
        self.lineEdit.setText(self.name)
        self.lineEdit_6.setText(self.ph)
        self.lineEdit_5.setText(self.address)
        self.lineEdit_4.setText(self.dob)
        c.close()
        db.close()

    def addImage(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file','c:/' , "Image files (*.jpg *.jpeg *.gif *.png)" )
        imagePath = fname[0]
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        c.execute("update seller set S_Image=%s where S_User_ID=%s",[imagePath,self.userid])
        c.execute("commit")
        c.execute("select S_Image from seller where S_User_ID=%s",[self.userid])
        result = c.fetchall()
        self.label.setScaledContents(True)
        self.label.setPixmap(QtGui.QPixmap(result[0][0]))
    
    def saveSale(self):
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        l1 = []
        flag = 1
        flag1 = 0
        check = []
        for i in range(self.tableWidget_3.rowCount()):
            dum = []
            t = []
            for j in range(self.tableWidget_3.columnCount()):
                dum.append(self.tableWidget_3.item(i,j).text())
                if (j==0 or j==1 or j==2):
                    t.append(self.tableWidget_3.item(i,j).text())
            check.append(t)
            if (("" not in dum) or (" " not in dum)):# and str(dum[2]).isalpha() and str(dum[3]).isnumeric() and str(dum[4]).isnumeric():
                l1.append(dum)
            else:
                flag = 0
                break
        if len(check)==len(set(list(map(str,check)))):
            flag1 = 1
        if flag == 1 and flag1 == 1 and len(l1)!=0:
            c.execute("select b_s_id, b_date, b_Cattle_Type, b_Milk_Qty, b_Amount, b_e_id from bill where b_s_id = %s",[self.id])
            l2 = c.fetchall()
            len_l1 = len(l1)
            len_l2 = len(l2)
            l3 = []
            l4 = []
            for i in range(len(l1)):
                dum = []
                for j in range(len(l1[i])):
                    dum.append(l1[i][j])
                l3.append(dum)
            for i in range(len(l2)):
                dum = []
                for j in range(len(l2[i])):
                    dum.append(l2[i][j])
                l4.append(dum)
            if len_l1 == len_l2:
                flag = 1
                i=0
                while (i < len_l2) and (flag!=0):
                    if l3[i]!=l4[i]:
                        if (l3[i][3]=="" or l3[i][3]==" "):
                            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Milk Quantity cannot be Empty')
                            flag = 0
                        elif int(l3[i][3])<0:
                            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Milk Quantity cannot be Negative')
                            flag = 0
                        elif len(l3[i][3])>15:
                            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Length of Milk Quantity cannot be More than 15')
                            flag = 0
                        else:
                            c.execute("update bill set b_Milk_Qty = %s where b_s_id = %s and b_date = %s and b_cattle_type = %s",[l3[i][3],self.id,l3[i][1],l3[i][2]])
                    if flag==0:
                        break
                    i+=1
            elif len_l1 > len_l2:
                #d = len_l1 - len_l2
                flag = 1
                i=0
                for i in range(len_l1):
                    if flag!=0 and (l3[i] not in l4):
                        if (l3[i][3]=="" or l3[i][3]==" "):
                            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Milk Quantity cannot be Empty')
                            flag = 0
                        elif int(l3[i][3])<0:
                            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Milk Quantity cannot be Negative')
                            flag = 0
                        elif len(l3[i][3])>15:
                            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Length of Milk Quantity cannot be More than 15')
                            flag = 0
                        else:
                            c.execute("insert into bill values( %s, %s, %s, %s, %s, %s)",[self.id,l3[i][4],l3[i][3],l3[i][1],l3[i][5],l3[i][2]])
                    else:
                        break
            else:
                for i in range(len(l4)):
                    if l4[i] not in l3:
                        c.execute("delete from bill where b_s_id = %s and b_date = %s and b_cattle_type = %s",[l4[i][0],l4[i][1],l4[i][2]])
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.setColumnCount(6)
            c.execute("commit")
            c.execute("select b_s_id, b_date, b_Cattle_Type, b_Milk_Qty, b_Amount, b_e_id from bill where b_s_id = %s",[self.id])
            f = c.fetchall()
            for r,rd in enumerate(f):
                if rd[0]==self.id:
                    self.tableWidget_3.setSizeIncrement(QtCore.QSize(891, 38))
                    self.tableWidget_3.insertRow(r)
                    for c,cd in enumerate(rd):
                        item = QtWidgets.QTableWidgetItem(str(cd))
                        if (c in [0,1,2,4,5]):
                            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                        self.tableWidget_3.setItem(r,c,item)
            self.tableWidget_3.resizeRowsToContents()
        elif flag==0 and flag1==1:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Check Entered Values and Cell cannot be Empty')
        elif flag==1 and flag1==0:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! You have already Entered the Cattle Type in Todays Sale, Try to modify the respective Milk Quantity')
        else:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Check Entered Values and Cell cannot be Empty. Also, You have already Entered the Cattle Type in Todays Sale, Try to modify the respective Milk Quantity')

    def cancelSale(self):
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        c.execute("select b_s_id, b_date, b_Cattle_Type, b_Milk_Qty, b_Amount, b_e_id from bill where b_s_id = %s",[self.id])
        f = c.fetchall()
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.setColumnCount(6)
        for r,rd in enumerate(f):
            if rd[0]==self.id:
                self.tableWidget_3.setSizeIncrement(QtCore.QSize(891, 38))
                self.tableWidget_3.insertRow(r)
                for c,cd in enumerate(rd):
                    item = QtWidgets.QTableWidgetItem(str(cd))
                    if (c in [0,1,2,4,5]):
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_3.setItem(r,c,item)
        self.tableWidget_3.resizeRowsToContents()

    def findSale(self):
        items = self.tableWidget_3.findItems(self.lineEdit_3.text(),QtCore.Qt.MatchContains)
        if items:
            l=[]
            for i in items:
                l.append(i.row()+1)
            l=list(set(l))
            l.sort()
            db = MySQLdb.connect(host="localhost",user="root",passwd="")
            c=db.cursor()
            c.execute("use project")
            c.execute("select b_s_id, b_date, b_Cattle_Type, b_Milk_Qty, b_Amount, b_e_id from bill where b_s_id = %s",[self.id])
            f=c.fetchall()
            ans=[]
            for i in range(len(l)):
                for j in range(len(f)):
                    if l[i]==j+1:
                        ans.append(f[j])
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.setColumnCount(6)                                #215, 70, 891, 601
            for r,rd in enumerate(ans):
                if rd[0]==self.id:
                    self.tableWidget_3.setSizeIncrement(QtCore.QSize(891, 38))
                    self.tableWidget_3.insertRow(r)
                    sel = rd[5]
                    for c,cd in enumerate(rd):
                        item = QtWidgets.QTableWidgetItem(str(cd))
                        if (c in [0,1,2,4,5]):
                            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                        self.tableWidget_3.setItem(r,c,item)
            self.tableWidget_3.resizeRowsToContents()     
        else:
            results = 'Found Nothing'
            QtWidgets.QMessageBox.information(self.tableWidget_3, 'Search Results', results)

    def tabulateSale(self):
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        c.execute("select b_s_id, b_date, b_Cattle_Type, b_Milk_Qty, b_Amount, b_e_id from bill where b_s_id = %s",[self.id])
        f=c.fetchall()
        self.tableWidget_3.setGeometry(QtCore.QRect(215, 70, 891, 601))
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.setColumnCount(6)
        for r,rd in enumerate(f):
            if rd[0]==self.id:
                self.tableWidget_3.setSizeIncrement(QtCore.QSize(891, 38))
                self.tableWidget_3.insertRow(r)
                for c,cd in enumerate(rd):
                    item = QtWidgets.QTableWidgetItem(str(cd))
                    if (c in [0,1,2,4,5]):
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_3.setItem(r,c,item)
        self.tableWidget_3.resizeRowsToContents()  
        self.lineEdit_3.setText("")

    def addSale(self):
        self.dat = date.today().strftime("%d/%m/%Y")
        f = [[self.id, self.dat, "", "", "", self.employee_id]]
        for r,rd in enumerate(f):
            if rd[0]==self.id:
                self.tableWidget_3.setSizeIncrement(QtCore.QSize(891, 38))
                self.tableWidget_3.insertRow(r)
                for c,cd in enumerate(rd):
                    item = QtWidgets.QTableWidgetItem(str(cd))
                    if (c in [0,1,5]):
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_3.setItem(r,c,item)
        self.tableWidget_3.resizeRowsToContents()

    def deleteSale(self):
        indexes = self.tableWidget_3.selectionModel().selectedRows()
        for index in sorted(indexes):
            self.tableWidget_3.removeRow(index.row())

    def setupUi(self, SellerPage1):
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        c.execute("select * from seller where s_user_id = %s",[self.userid])
        result = c.fetchall()
        self.name = result[0][0]
        self.id = result[0][1]
        self.gender = result[0][2]
        self.dob = result[0][3]
        self.salary = result[0][4]
        self.employee_id = result[0][5]
        self.ph = result[0][6]
        self.address = result[0][7]
        SellerPage1.setObjectName("SellerPage1")
        self.SellerPage1=SellerPage1
        #SellerPage1.resize(1546, 929)
        SellerPage1.setFixedSize(1546, 929)
        SellerPage1.setWindowFlags(SellerPage1.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint) # Make a Note of it
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Logo/Images/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SellerPage1.setWindowIcon(icon)
        SellerPage1.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.centralwidget = QtWidgets.QWidget(SellerPage1)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 70, 1526, 791))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 10, 211, 211))
        self.label.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.label.setText("")
        c.execute("select S_Image from seller where S_User_Id = %s",[self.userid])   #################
        imagePath = c.fetchall()
        self.label.setPixmap(QtGui.QPixmap(imagePath[0][0]))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setGeometry(QtCore.QRect(220, 0, 16, 791))
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 230, 211, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.tabWidget = QtWidgets.QTabWidget(self.frame)
        self.tabWidget.setGeometry(QtCore.QRect(234, 10, 1287, 771))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("background-color: rgb(141, 211, 0);")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_12 = QtWidgets.QLabel(self.tab)
        self.label_12.setGeometry(QtCore.QRect(70, 540, 401, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.tab)
        self.label_13.setGeometry(QtCore.QRect(70, 40, 401, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.label_24 = QtWidgets.QLabel(self.tab)
        self.label_24.setGeometry(QtCore.QRect(90, 640, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.label_24.setObjectName("label_24")
        self.lineEdit_19 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_19.setGeometry(QtCore.QRect(340, 640, 241, 41))
        self.lineEdit_19.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_19.setEchoMode(QtWidgets.QLineEdit.Password)   # Make a Note of it
        self.lineEdit_19.setAlignment(QtCore.Qt.AlignCenter)         # Make a Note of it
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.lineEdit_18 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_18.setGeometry(QtCore.QRect(300, 590, 281, 41))
        self.lineEdit_18.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_18.setEchoMode(QtWidgets.QLineEdit.Password)   # Make a Note of it
        self.lineEdit_18.setAlignment(QtCore.Qt.AlignCenter)         # Make a Note of it
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.label_23 = QtWidgets.QLabel(self.tab)
        self.label_23.setGeometry(QtCore.QRect(90, 590, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.label_16 = QtWidgets.QLabel(self.tab)
        self.label_16.setGeometry(QtCore.QRect(90, 330, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_7.setGeometry(QtCore.QRect(450, 330, 361, 41))
        self.lineEdit_7.setStyleSheet("background-color: rgb(159, 159, 159);")
        self.lineEdit_7.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_7.setText(self.gender)
        self.lineEdit_7.setReadOnly(True)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(90, 230, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_10 = QtWidgets.QLabel(self.tab)
        self.label_10.setGeometry(QtCore.QRect(90, 280, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(450, 80, 361, 41))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setText(self.name)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_5.setGeometry(QtCore.QRect(450, 230, 361, 41))
        self.lineEdit_5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_5.setText(self.address)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_2.setGeometry(QtCore.QRect(450, 130, 361, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color: rgb(159, 159, 159);")
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setText(self.id)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_13 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_13.setGeometry(QtCore.QRect(450, 430, 361, 41))
        self.lineEdit_13.setStyleSheet("background-color: rgb(159, 159, 159);")
        self.lineEdit_13.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_13.setText(self.employee_id)
        self.lineEdit_13.setReadOnly(True)
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_4.setGeometry(QtCore.QRect(450, 280, 361, 41))
        self.lineEdit_4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_4.setText(self.dob)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_18 = QtWidgets.QLabel(self.tab)
        self.label_18.setGeometry(QtCore.QRect(90, 480, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(90, 130, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.lineEdit_12 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_12.setGeometry(QtCore.QRect(450, 380, 361, 41))
        self.lineEdit_12.setStyleSheet("background-color: rgb(159, 159, 159);")
        self.lineEdit_12.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_12.setText(self.salary)
        self.lineEdit_12.setReadOnly(True)
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_9.setGeometry(QtCore.QRect(450, 480, 361, 41))
        self.lineEdit_9.setStyleSheet("background-color: rgb(159, 159, 159);")
        self.lineEdit_9.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_9.setText(self.userid)
        self.lineEdit_9.setReadOnly(True)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.label_22 = QtWidgets.QLabel(self.tab)
        self.label_22.setGeometry(QtCore.QRect(90, 380, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName("label_22")
        self.label_25 = QtWidgets.QLabel(self.tab)
        self.label_25.setGeometry(QtCore.QRect(90, 430, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_25.setFont(font)
        self.label_25.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_25.setAlignment(QtCore.Qt.AlignCenter)
        self.label_25.setObjectName("label_25")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(90, 80, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(90, 180, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_6.setGeometry(QtCore.QRect(450, 180, 361, 41))
        self.lineEdit_6.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_6.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_6.setText(self.ph)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.label_14 = QtWidgets.QLabel(self.tab)
        self.label_14.setGeometry(QtCore.QRect(850, 40, 401, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab)
        self.pushButton_7.setGeometry(QtCore.QRect(870, 79, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setStyleSheet("background-color: rgb(0, 0, 255);\n"
"color: rgb(255, 255, 255);")
        self.pushButton_7.clicked.connect(self.addImage)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_18 = QtWidgets.QPushButton(self.tab)
        self.pushButton_18.setGeometry(QtCore.QRect(530, 690, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_18.setFont(font)
        self.pushButton_18.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.pushButton_18.clicked.connect(self.saveProfile)
        self.pushButton_18.setObjectName("pushButton_18")
        self.pushButton_19 = QtWidgets.QPushButton(self.tab)
        self.pushButton_19.setGeometry(QtCore.QRect(690, 690, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_19.setFont(font)
        self.pushButton_19.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.pushButton_19.clicked.connect(self.cancelProfile)
        self.pushButton_19.setObjectName("pushButton_19")
        self.tabWidget.addTab(self.tab, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tableWidget_3 = QtWidgets.QTableWidget(self.tab_4)
        self.tableWidget_3.setGeometry(QtCore.QRect(215, 70, 891, 601))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tableWidget_3.setFont(font)
        self.tableWidget_3.setStyleSheet("background-color: rgb(255, 170, 127);\n"
"border-color: rgb(0, 0, 0);")
        self.tableWidget_3.setLineWidth(1)
        self.tableWidget_3.setTabKeyNavigation(True)
        self.tableWidget_3.setWordWrap(True)
        self.tableWidget_3.setCornerButtonEnabled(True)
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.setColumnCount(6)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setMinimumSize(QtCore.QSize(891, 31))
        self.tableWidget_3.setMaximumSize(QtCore.QSize(891, 601))
        self.tableWidget_3.setSizeIncrement(QtCore.QSize(891, 38))
        self.tableWidget_3.setBaseSize(QtCore.QSize(891, 38))
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_3.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_3.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_3.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_3.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_3.setHorizontalHeaderItem(5, item)
        self.tableWidget_3.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget_3.horizontalHeader().setDefaultSectionSize(145)
        self.tableWidget_3.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget_3.horizontalHeader().setStretchLastSection(False)

        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        c.execute("select b_s_id, b_date, b_Cattle_Type, b_Milk_Qty, b_Amount, b_e_id from bill where b_s_id = %s",[self.id])
        f = c.fetchall()
        for r,rd in enumerate(f):
            if rd[0]==self.id:
                self.tableWidget_3.setSizeIncrement(QtCore.QSize(891, 38))
                self.tableWidget_3.insertRow(r)
                for c,cd in enumerate(rd):
                    item = QtWidgets.QTableWidgetItem(str(cd))
                    if (c in [0,1,2,4,5]):
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_3.setItem(r,c,item)
        self.tableWidget_3.resizeRowsToContents()


        self.label_6 = QtWidgets.QLabel(self.tab_4)
        self.label_6.setGeometry(QtCore.QRect(430, 36, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab_4)
        self.lineEdit_3.setGeometry(QtCore.QRect(530, 30, 221, 31))
        self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_5.setGeometry(QtCore.QRect(760, 31, 41, 30))
        self.pushButton_5.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.pushButton_5.clicked.connect(self.findSale)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_6.setGeometry(QtCore.QRect(810, 31, 61, 30))
        self.pushButton_6.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.pushButton_6.clicked.connect(self.tabulateSale)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_20 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_20.setGeometry(QtCore.QRect(700, 680, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_20.setFont(font)
        self.pushButton_20.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.pushButton_20.clicked.connect(self.cancelSale)
        self.pushButton_20.setObjectName("pushButton_20")
        self.pushButton_21 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_21.setGeometry(QtCore.QRect(540, 680, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_21.setFont(font)
        self.pushButton_21.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.pushButton_21.clicked.connect(self.saveSale)
        self.pushButton_21.setObjectName("pushButton_21")

        self.pushButton_30 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_30.setGeometry(QtCore.QRect(380, 680, 95, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_30.setFont(font)
        self.pushButton_30.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.pushButton_30.clicked.connect(self.addSale)
        self.pushButton_30.setObjectName("pushButton_30")
        self.pushButton_31 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_31.setGeometry(QtCore.QRect(860, 680, 115, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_31.setFont(font)
        self.pushButton_31.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.pushButton_31.clicked.connect(self.deleteSale)
        self.pushButton_31.setObjectName("pushButton_31")

        self.tabWidget.addTab(self.tab_4, "")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(670, 10, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_3.setObjectName("label_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(1440, 10, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 0, 0);")
        self.pushButton_4.clicked.connect(self.logout)
        self.pushButton_4.setObjectName("pushButton_4")
        SellerPage1.setCentralWidget(self.centralwidget)
        self.retranslateUi(SellerPage1)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(SellerPage1)

    def retranslateUi(self, SellerPage1):
        _translate = QtCore.QCoreApplication.translate
        SellerPage1.setWindowTitle(_translate("SellerPage1", "Seller Page"))
        self.label_2.setText(_translate("SellerPage1", self.name))
        self.label_12.setText(_translate("SellerPage1", "CHANGE PASSWORD :"))
        self.label_13.setText(_translate("SellerPage1", "DETAILS :"))
        self.label_24.setText(_translate("SellerPage1", "RE-ENTER PASSWORD"))
        self.label_23.setText(_translate("SellerPage1", "PASSWORD"))
        self.label_16.setText(_translate("SellerPage1", "GENDER"))
        self.label_8.setText(_translate("SellerPage1", "ADDRESS"))
        self.label_10.setText(_translate("SellerPage1", "DATE OF BIRTH"))
        self.label_18.setText(_translate("SellerPage1", "USER ID"))
        self.label_5.setText(_translate("SellerPage1", "SELLER ID"))
        self.label_22.setText(_translate("SellerPage1", "SALARY"))
        self.label_25.setText(_translate("SellerPage1", "EMPLOYEE ID"))
        self.label_4.setText(_translate("SellerPage1", "NAME"))
        self.label_7.setText(_translate("SellerPage1", "PH. NO."))
        self.label_14.setText(_translate("SellerPage1", "PROFILE PHOTO :"))
        self.pushButton_7.setText(_translate("SellerPage1", "Click Here To Open The File Location"))
        self.pushButton_18.setText(_translate("SellerPage1", "SAVE"))
        self.pushButton_19.setText(_translate("SellerPage1", "CANCEL"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("SellerPage1", "My Profile"))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("SellerPage1", "Seller ID"))
        item = self.tableWidget_3.horizontalHeaderItem(1)
        item.setText(_translate("SellerPage1", "Date"))
        item = self.tableWidget_3.horizontalHeaderItem(2)
        item.setText(_translate("SellerPage1", "Cattle Type"))
        item = self.tableWidget_3.horizontalHeaderItem(3)
        item.setText(_translate("SellerPage1", "Milk Quantity"))
        item = self.tableWidget_3.horizontalHeaderItem(4)
        item.setText(_translate("SellerPage1", "PRICE(per Ltrs)"))
        item = self.tableWidget_3.horizontalHeaderItem(5)
        item.setText(_translate("SellerPage1", "Employee ID"))
        self.label_6.setText(_translate("SellerPage1", "SEARCH"))
        self.pushButton_5.setText(_translate("SellerPage1", "Ok"))
        self.pushButton_6.setText(_translate("SellerPage1", "Clear"))
        self.pushButton_20.setText(_translate("SellerPage1", "CANCEL"))
        self.pushButton_21.setText(_translate("SellerPage1", "SAVE"))
        self.pushButton_30.setText(_translate("SellerPage1", "ADD SALE"))
        self.pushButton_31.setText(_translate("SellerPage1", "DELETE SALE"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("SellerPage1", "Purchase Report"))
        self.label_3.setText(_translate("SellerPage1", "WELCOME"))
        self.pushButton_4.setText(_translate("SellerPage1", "LOGOUT"))

import AdminR
import LogoR