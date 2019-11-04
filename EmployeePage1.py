# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import MySQLdb
from LoginPage import Ui_LoginPage
import re
from datetime import date

class Ui_EmployeePage1(object):

    def __init__( self, userid, password):                                           # Make a Note of it
        self.userid=userid
        self.password=password
        
    def logout(self):
        self.LP = QtWidgets.QMainWindow()
        self.ui = Ui_LoginPage()
        self.ui.setupUi(self.LP)
        self.EmployeePage1.close()
        self.LP.show()

    def saveProfile(self):
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        newName = self.lineEdit.text()
        newPh = self.lineEdit_5.text()
        newAddress = self.lineEdit_9.text()
        newDob = self.lineEdit_11.text()
        password = self.lineEdit_18.text()
        re_password = self.lineEdit_19.text()
        year1 = int(self.lineEdit_6.text()[-4:])
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
                QtWidgets.QMessageBox.information(self.lineEdit_10, 'Error','Sorry, Entered Password and Re-Entered Password Doesnot Match')
            elif (newName=="") or (newPh=="") or (newDob==""):
                QtWidgets.QMessageBox.information(self.lineEdit_6, 'Error','Sorry! Name, Phone No., DOB cannot be Empty')
            elif check1!=1 and newDob!="":
                QtWidgets.QMessageBox.information(self.lineEdit_4, 'Error','Sorry! Check Date format(should be dd/mm/yyyy)')
            elif check1==1 and (this_year-year)<=18 or (year1-year)<=18:
                QtWidgets.QMessageBox.information(self.lineEdit_4, 'Error','Sorry! Check your Date Of Birth')
            elif check!=1:
                QtWidgets.QMessageBox.information(self.lineEdit_6, 'Error','Sorry! Check your Phone Number')
            elif (len(password)>15):
                QtWidgets.QMessageBox.information(self.lineEdit_10, 'Error','Sorry! Length of Password cannot be more than 15')
            elif (len(newName)>40):
                QtWidgets.QMessageBox.information(self.lineEdit_13, 'Error','Sorry! Length of Name cannot be more than 40')
            elif (len(newAddress)>100):
                QtWidgets.QMessageBox.information(self.lineEdit_5, 'Error','Sorry! Length of Address cannot be more than 100')
            else:
                if password=="" and re_password=="":
                    c.execute("update employee set e_name = %s, e_ph = %s, e_address = %s, e_dob = %s where e_user_id = %s",[newName,newPh,newAddress,newDob,self.userid])
                else:
                    self.password=password
                    c.execute("update employee set e_name = %s, e_ph = %s, e_address = %s, e_dob = %s, e_password = %s where e_user_id = %s",[newName,newPh,newAddress,newDob,password,self.userid])
                    c.execute("update login set password = %s where user_id = %s",[password,self.userid])
                c.execute("commit")    
                QtWidgets.QMessageBox.information(self.lineEdit_10, 'Pop-Up','Saved Successfully!!!')
                c.close()
                db.close()
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        c.execute("select * from employee where e_user_id = %s",[self.userid])
        result = c.fetchall()
        self.id = result[0][1]
        self.name = result[0][0]
        self.gender = result[0][2]
        self.ph = result[0][6]
        self.dob = result[0][3]
        self.department = result[0][4]
        self.admin_id = result[0][5]
        self.address = result[0][9]
        self.salary = result[0][7]
        self.doj = result[0][8]
        self.job = result[0][10]
        c.close()
        db.close()
        self.lineEdit_18.setText("")
        self.lineEdit_19.setText("")

    def cancelProfile(self):
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        c.execute("select * from employee where e_user_id = %s",[self.userid])
        result = c.fetchall()
        self.name = result[0][0]
        self.ph = result[0][6]
        self.dob = result[0][3]
        self.address = result[0][9]
        self.lineEdit.setText(self.name)
        self.lineEdit_5.setText(self.ph)
        self.lineEdit_9.setText(self.address)
        self.lineEdit_11.setText(self.dob)
        c.close()
        db.close()

    def addImage(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file','c:/' , "Image files (*.jpg *.jpeg *.gif *.png)" )
        imagePath = fname[0]
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        c.execute("update employee set E_Image=%s where E_User_ID=%s",[imagePath,self.userid])
        c.execute("commit")
        c.execute("select E_Image from employee where E_User_ID=%s",[self.userid])
        result = c.fetchall()
        self.label.setScaledContents(True)
        self.label.setPixmap(QtGui.QPixmap(result[0][0]))
    
    def findDepartment(self):
        items = self.tableWidget_2.findItems(self.lineEdit_2.text(),QtCore.Qt.MatchContains)
        if items:
            l=[]
            for i in items:
                l.append(i.row()+1)
            l=list(set(l))
            l.sort()
            db = MySQLdb.connect(host="localhost",user="root",passwd="")
            c=db.cursor()
            c.execute("use project")
            c.execute("select * from department")
            f=c.fetchall()
            ans=[]
            for i in range(len(l)):
                for j in range(len(f)):
                    if l[i]==j+1:
                        ans.append(f[j])
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.setColumnCount(3)
            for r,rd in enumerate(ans):
                self.tableWidget_2.setSizeIncrement(QtCore.QSize(621, 38))
                self.tableWidget_2.insertRow(r)
                for c,cd in enumerate(rd):
                    self.tableWidget_2.setItem(r,c,QtWidgets.QTableWidgetItem(str(cd))) 
            self.tableWidget_2.resizeRowsToContents()     
        else:
            results = 'Found Nothing'
            QtWidgets.QMessageBox.information(self.tableWidget_2, 'Search Results', results)

    def tabulateDepartment(self):
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        c.execute("select * from department")
        f=c.fetchall()
        self.tableWidget_2.setGeometry(QtCore.QRect(330, 160, 621, 401))
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(3)
        for r,rd in enumerate(f):
            self.tableWidget_2.setSizeIncrement(QtCore.QSize(621, 38))
            self.tableWidget_2.insertRow(r)
            for c,cd in enumerate(rd):
                self.tableWidget_2.setItem(r,c,QtWidgets.QTableWidgetItem(str(cd)))
        self.tableWidget_2.resizeRowsToContents()  
        self.lineEdit_2.setText("")

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
            c.execute("select b_s_id, b_date, b_Cattle_Type, b_Milk_Qty, b_Amount, b_e_id from bill where b_e_id = %s",[self.id])
            f=c.fetchall()
            ans=[]
            for i in range(len(l)):
                for j in range(len(f)):
                    if l[i]==j+1:
                        ans.append(f[j])
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.setColumnCount(6)                                #215, 70, 891, 601
            for r,rd in enumerate(ans):
                if rd[5]==self.id:
                    self.tableWidget_3.setSizeIncrement(QtCore.QSize(891, 38))
                    self.tableWidget_3.insertRow(r)
                    for c,cd in enumerate(rd):
                        item = QtWidgets.QTableWidgetItem(str(cd))
                        self.tableWidget_3.setItem(r,c,item)
            self.tableWidget_3.resizeRowsToContents()     
        else:
            results = 'Found Nothing'
            QtWidgets.QMessageBox.information(self.tableWidget_3, 'Search Results', results)

    def tabulateSale(self):
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        c.execute("select b_s_id, b_date, b_Cattle_Type, b_Milk_Qty, b_Amount, b_e_id from bill where b_e_id = %s",[self.id])
        f=c.fetchall()
        self.tableWidget_3.setGeometry(QtCore.QRect(205, 70, 891, 601))
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.setColumnCount(6)
        for r,rd in enumerate(f):
            if rd[5]==self.id:
                self.tableWidget_3.setSizeIncrement(QtCore.QSize(891, 38))
                self.tableWidget_3.insertRow(r)
                for c,cd in enumerate(rd):
                    item = QtWidgets.QTableWidgetItem(str(cd))
                    self.tableWidget_3.setItem(r,c,item)
        self.tableWidget_3.resizeRowsToContents()  
        self.lineEdit_3.setText("")

    def saveSeller(self):
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        l1 = []
        flag = 1
        flag1 = 0
        check = []
        for i in range(self.tableWidget_4.rowCount()):
            dum = []
            for j in range(self.tableWidget_4.columnCount()):
                dum.append(self.tableWidget_4.item(i,j).text())
                if (j==0):
                    check.append(self.tableWidget_4.item(i,j).text())
            c.execute("select E_Id from employee where E_Id = %s and E_D_ID = %s",[dum[5],"Purchase"])
            if len(c.fetchall())==0:
                insert1=1
            else:
                insert1=0
            if re.match("^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$",dum[3]):
                b = True
            else:
                b = False
            if re.match("$seller",str(dum[2])):
                b1 = True
            else:
                b1 = False
            if (("" not in dum) or (" " not in dum)):# and b and b1 and insert1==0 and (len(dum[6])==10 and str(dum[6]).isnumeric()):
                l1.append(dum)
            else:
                flag = 0
                break
        if len(check)==len(set(check)):
            flag1 = 1
        if flag == 1 and flag1 == 1:
            c.execute("select s_id, s_name, s_user_id, s_dob, s_salary, s_e_id, s_ph, s_address from seller where s_e_id = %s",[self.id])
            l2 = c.fetchall()
            len_l1 = len(l1)
            len_l2 = len(l2)
            if len_l1 == len_l2:
                flag = 1
                i=0
                while (i < len_l2) and (flag!=0):
                    #while (j < len(l1[i])) and (flag!=0):
                    if l1[i]!=list(l2[i]):
                        if len(l1[i][0])>15 or len(l1[i][1])>40 or len(l1[i][2])>15 or len(l1[i][3])>15 or len(l1[i][4])>15 or len(l1[i][5])>15 or len(l1[i][6])>15 or len(l1[i][7])>100:
                            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Check the Length of Entered Values')
                            flag = 0
                        else:
                            c.execute("update seller set s_salary = %s where s_id = %s",[l1[i][4],l1[i][0]])
                    if flag==0:
                        break
                    i+=1
            elif len_l1 > len_l2:
                d = len_l1 - len_l2
                flag = 1
                i=0
                for i in range(d):
                    if flag!=0:
                        if len(l1[i][0])>15 or len(l1[i][1])>40 or len(l1[i][2])>15 or len(l1[i][3])>15 or len(l1[i][4])>15 or len(l1[i][5])>15 or len(l1[i][6])>15 or len(l1[i][7])>100:
                            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Check the Length of Entered Values')
                            flag = 0
                        else:
                            imagePath = "D:/VIT/Database Management System/Project/PyQT/Images/Admin.png"
                            c.execute("insert into seller values( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[l1[i][1],l1[i][0],"",l1[i][3],l1[i][4],l1[i][5],l1[i][6],l1[i][7],l1[i][2],l1[i][1],imagePath])
                            c.execute("insert into login values(%s,%s)",[l1[i][2],l1[i][1]])
                    else:
                        break
            else:
                for i in range(len(l2)):
                    if list(l2[i]) not in l1:
                        c.execute("delete from seller where s_id = %s",[l2[i][0]])
                        c.execute("delete from bill where b_s_id = %s",[l2[i][0]])
                        c.execute("delete from login where user_id = %s",[l2[i][2]])
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.setColumnCount(8)
            c.execute("commit")
            c.execute("select s_id, s_name, s_user_id, s_dob, s_salary, s_e_id, s_ph, s_address from seller where s_e_id = %s",[self.id])
            f = c.fetchall()
            for r,rd in enumerate(f):
                if rd[5]==self.id:
                    self.tableWidget_4.setSizeIncrement(QtCore.QSize(1181, 38))
                    self.tableWidget_4.insertRow(r)
                    for c,cd in enumerate(rd):
                        item = QtWidgets.QTableWidgetItem(str(cd))
                        if (c in [0,1,2,3,5,6,7]):
                            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                        self.tableWidget_4.setItem(r,c,item)
            self.tableWidget_4.resizeRowsToContents()
        elif flag==0 and flag1==1:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Check Entered Values and Cell cannot be Empty')
        elif flag==1 and flag1==0:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! You have already Entered the Cattle Type in Todays Sale, Try to modify the respective Milk Quantity')
        else:
            QtWidgets.QMessageBox.information(self.lineEdit, 'Error','Sorry! Check Entered Values and Cell cannot be Empty. Also, You have already Entered the Cattle Type in Todays Sale, Try to modify the respective Milk Quantity')

    def cancelSeller(self):
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        c.execute("select s_id, s_name, s_user_id, s_dob, s_salary, s_e_id, s_ph, s_address from seller where s_e_id = %s",[self.id])
        f = c.fetchall()
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.setColumnCount(8)
        for r,rd in enumerate(f):
            if rd[5]==self.id:
                self.tableWidget_4.setSizeIncrement(QtCore.QSize(1181, 38))
                self.tableWidget_4.insertRow(r)
                for c,cd in enumerate(rd):
                    item = QtWidgets.QTableWidgetItem(str(cd))
                    if (c in [0,1,2,3,5,6,7]):
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_4.setItem(r,c,item)
        self.tableWidget_4.resizeRowsToContents()

    def findSeller(self):
        items = self.tableWidget_4.findItems(self.lineEdit_14.text(),QtCore.Qt.MatchContains)
        if items:
            l=[]
            for i in items:
                l.append(i.row()+1)
            l=list(set(l))
            l.sort()
            db = MySQLdb.connect(host="localhost",user="root",passwd="")
            c=db.cursor()
            c.execute("use project")
            c.execute("select s_id, s_name, s_user_id, s_dob, s_salary, s_e_id, s_ph, s_address from seller where s_e_id = %s",[self.id])
            f=c.fetchall()
            ans=[]
            for i in range(len(l)):
                for j in range(len(f)):
                    if l[i]==j+1:
                        ans.append(f[j])
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.setColumnCount(8)                                #215, 70, 891, 601
            for r,rd in enumerate(ans):
                if rd[5]==self.id:
                    self.tableWidget_4.setSizeIncrement(QtCore.QSize(1181, 38))
                    self.tableWidget_4.insertRow(r)
                    for c,cd in enumerate(rd):
                        item = QtWidgets.QTableWidgetItem(str(cd))
                        if (c in [0,1,2,3,5,6,7]):
                            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                        self.tableWidget_4.setItem(r,c,item)
            self.tableWidget_4.resizeRowsToContents()     
        else:
            results = 'Found Nothing'
            QtWidgets.QMessageBox.information(self.tableWidget_4, 'Search Results', results)

    def tabulateSeller(self):
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        c.execute("select s_id, s_name, s_user_id, s_dob, s_salary, s_e_id, s_ph, s_address from seller where s_e_id = %s",[self.id])
        f=c.fetchall()
        self.tableWidget_4.setGeometry(QtCore.QRect(50, 80, 1181, 591))
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.setColumnCount(8)
        for r,rd in enumerate(f):
            if rd[5]==self.id:
                self.tableWidget_4.setSizeIncrement(QtCore.QSize(1181, 38))
                self.tableWidget_4.insertRow(r)
                for c,cd in enumerate(rd):
                    item = QtWidgets.QTableWidgetItem(str(cd))
                    if (c in [0,1,2,3,5,6,7]):
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_4.setItem(r,c,item)
        self.tableWidget_4.resizeRowsToContents()  
        self.lineEdit_14.setText("")

    def addSeller(self):
        f = [[ "", "", "", "", "", self.id, "", ""]]
        for r,rd in enumerate(f):
            if rd[5]==self.id:
                self.tableWidget_4.setSizeIncrement(QtCore.QSize(1181, 38))
                self.tableWidget_4.insertRow(r)
                for c,cd in enumerate(rd):
                    item = QtWidgets.QTableWidgetItem(str(cd))
                    if (c == 5):
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_4.setItem(r,c,item)
        self.tableWidget_4.resizeRowsToContents()

    def deleteSeller(self):
        indexes = self.tableWidget_4.selectionModel().selectedRows()
        for index in sorted(indexes):
            self.tableWidget_4.removeRow(index.row())

    def setupUi(self, EmployeePage1):
        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        c.execute("select * from employee where e_user_id = %s",[self.userid])
        result = c.fetchall()
        self.id = result[0][1]
        self.name = result[0][0]
        self.gender = result[0][2]
        self.ph = result[0][6]
        self.dob = result[0][3]
        self.department = result[0][4]
        self.admin_id = result[0][5]
        self.address = result[0][9]
        self.salary = result[0][7]
        self.doj = result[0][8]
        self.job = result[0][10]
        EmployeePage1.setObjectName("EmployeePage1")
        self.EmployeePage1=EmployeePage1
        #EmployeePage1.resize(1546, 929)
        EmployeePage1.setFixedSize(1546, 929)
        EmployeePage1.setWindowFlags(EmployeePage1.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint) # Make a Note of it
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Logo/Images/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        EmployeePage1.setWindowIcon(icon)
        EmployeePage1.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.centralwidget = QtWidgets.QWidget(EmployeePage1)
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
        c.execute("select E_Image from employee where E_User_Id = %s",[self.userid])   #################
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
        self.label_2.setGeometry(QtCore.QRect(10, 230, 111, 20))
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
        self.label_12.setGeometry(QtCore.QRect(190, 510, 401, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.tab)
        self.label_13.setGeometry(QtCore.QRect(190, 60, 401, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.label_11 = QtWidgets.QLabel(self.tab)
        self.label_11.setGeometry(QtCore.QRect(730, 220, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.lineEdit_13 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_13.setGeometry(QtCore.QRect(940, 320, 281, 41))
        self.lineEdit_13.setStyleSheet("background-color: rgb(159, 159, 159);")
        self.lineEdit_13.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_13.setText(self.gender)
        self.lineEdit_13.setReadOnly(True)
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.label_24 = QtWidgets.QLabel(self.tab)
        self.label_24.setGeometry(QtCore.QRect(210, 620, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.label_24.setObjectName("label_24")
        self.lineEdit_17 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_17.setGeometry(QtCore.QRect(420, 320, 281, 41))
        self.lineEdit_17.setStyleSheet("background-color: rgb(159, 159, 159);")
        self.lineEdit_17.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_17.setText(self.userid)
        self.lineEdit_17.setReadOnly(True)
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(730, 170, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_6.setGeometry(QtCore.QRect(420, 370, 281, 41))
        self.lineEdit_6.setStyleSheet("background-color: rgb(159, 159, 159);")
        self.lineEdit_6.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_6.setText(self.doj)
        self.lineEdit_6.setReadOnly(True)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.label_10 = QtWidgets.QLabel(self.tab)
        self.label_10.setGeometry(QtCore.QRect(730, 270, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_8.setGeometry(QtCore.QRect(940, 170, 281, 41))
        self.lineEdit_8.setStyleSheet("background-color: rgb(159, 159, 159);")
        self.lineEdit_8.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_8.setText(self.id)
        self.lineEdit_8.setReadOnly(True)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.lineEdit_19 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_19.setGeometry(QtCore.QRect(460, 620, 241, 41))
        self.lineEdit_19.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_19.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_19.setText("")
        self.lineEdit_19.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.lineEdit_12 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_12.setGeometry(QtCore.QRect(940, 120, 281, 41))
        self.lineEdit_12.setStyleSheet("background-color: rgb(159, 159, 159);")
        self.lineEdit_12.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_12.setText(self.job)
        self.lineEdit_12.setReadOnly(True)
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.lineEdit_18 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_18.setGeometry(QtCore.QRect(420, 570, 281, 41))
        self.lineEdit_18.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_18.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_18.setText("")
        self.lineEdit_18.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.label_15 = QtWidgets.QLabel(self.tab)
        self.label_15.setGeometry(QtCore.QRect(730, 120, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_5.setGeometry(QtCore.QRect(940, 220, 281, 41))
        self.lineEdit_5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_5.setText(self.ph)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_9.setGeometry(QtCore.QRect(420, 420, 281, 41))
        self.lineEdit_9.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_9.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_9.setText(self.address)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setGeometry(QtCore.QRect(210, 370, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.lineEdit_11 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_11.setGeometry(QtCore.QRect(940, 270, 281, 41))
        self.lineEdit_11.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_11.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_11.setText(self.dob)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.label_17 = QtWidgets.QLabel(self.tab)
        self.label_17.setGeometry(QtCore.QRect(210, 170, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(210, 120, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_4.setGeometry(QtCore.QRect(420, 170, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setStyleSheet("background-color: rgb(159, 159, 159);")
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_4.setText(self.department)
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_7.setGeometry(QtCore.QRect(420, 270, 281, 41))
        self.lineEdit_7.setStyleSheet("background-color: rgb(159, 159, 159);")
        self.lineEdit_7.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_7.setText(self.salary)
        self.lineEdit_7.setReadOnly(True)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.label_18 = QtWidgets.QLabel(self.tab)
        self.label_18.setGeometry(QtCore.QRect(730, 320, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.label_22 = QtWidgets.QLabel(self.tab)
        self.label_22.setGeometry(QtCore.QRect(210, 320, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName("label_22")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(420, 120, 281, 41))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setText(self.name)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_10.setGeometry(QtCore.QRect(420, 220, 281, 41))
        self.lineEdit_10.setStyleSheet("background-color: rgb(159, 159, 159);")
        self.lineEdit_10.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_10.setText(self.admin_id)
        self.lineEdit_10.setReadOnly(True)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.label_14 = QtWidgets.QLabel(self.tab)
        self.label_14.setGeometry(QtCore.QRect(210, 220, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.label_16 = QtWidgets.QLabel(self.tab)
        self.label_16.setGeometry(QtCore.QRect(210, 270, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.label_23 = QtWidgets.QLabel(self.tab)
        self.label_23.setGeometry(QtCore.QRect(210, 570, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(210, 420, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("background-color: rgb(170, 85, 255);")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_20 = QtWidgets.QLabel(self.tab)
        self.label_20.setGeometry(QtCore.QRect(730, 391, 401, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.pushButton_11 = QtWidgets.QPushButton(self.tab)
        self.pushButton_11.setGeometry(QtCore.QRect(810, 440, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_11.setFont(font)
        self.pushButton_11.setStyleSheet("background-color: rgb(0, 0, 255);\n"
"color: rgb(255, 255, 255);")
        self.pushButton_11.clicked.connect(self.addImage)
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_19 = QtWidgets.QPushButton(self.tab)
        self.pushButton_19.setGeometry(QtCore.QRect(730, 690, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_19.setFont(font)
        self.pushButton_19.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.pushButton_19.clicked.connect(self.cancelProfile)
        self.pushButton_19.setObjectName("pushButton_19")
        self.pushButton_18 = QtWidgets.QPushButton(self.tab)
        self.pushButton_18.setGeometry(QtCore.QRect(570, 690, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_18.setFont(font)
        self.pushButton_18.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.pushButton_18.clicked.connect(self.saveProfile)
        self.pushButton_18.setObjectName("pushButton_18")
        self.tabWidget.addTab(self.tab, "")
        if self.department=="Purchase":
            self.tab_2 = QtWidgets.QWidget()
            self.tab_2.setObjectName("tab_2")
            self.tableWidget_4 = QtWidgets.QTableWidget(self.tab_2)
            self.tableWidget_4.setGeometry(QtCore.QRect(50, 80, 1181, 591))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            self.tableWidget_4.setFont(font)
            self.tableWidget_4.setStyleSheet("background-color: rgb(255, 170, 127);\n"
    "border-color: rgb(0, 0, 0);")
            self.tableWidget_4.setLineWidth(1)
            self.tableWidget_4.setTabKeyNavigation(True)
            self.tableWidget_4.setWordWrap(True)
            self.tableWidget_4.setCornerButtonEnabled(True)
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.setColumnCount(8)
            self.tableWidget_4.setObjectName("tableWidget_4")
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.tableWidget_4.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.tableWidget_4.setHorizontalHeaderItem(1, item)
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.tableWidget_4.setHorizontalHeaderItem(2, item)
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.tableWidget_4.setHorizontalHeaderItem(3, item)
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.tableWidget_4.setHorizontalHeaderItem(4, item)
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(9)
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.tableWidget_4.setHorizontalHeaderItem(5, item)
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(9)
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.tableWidget_4.setHorizontalHeaderItem(6, item)
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(9)
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.tableWidget_4.setHorizontalHeaderItem(7, item)
            self.tableWidget_4.horizontalHeader().setCascadingSectionResizes(True)
            self.tableWidget_4.horizontalHeader().setDefaultSectionSize(145)
            self.tableWidget_4.horizontalHeader().setSortIndicatorShown(True)
            self.tableWidget_4.horizontalHeader().setStretchLastSection(False)

            db = MySQLdb.connect(host="localhost",user="root",passwd="")
            c=db.cursor()
            c.execute("use project")
            c.execute("select s_id, s_name, s_user_id, s_dob, s_salary, s_e_id, s_ph, s_address from seller where s_e_id = %s",[self.id])
            f=c.fetchall()
            for r,rd in enumerate(f):
                if rd[5]==self.id:
                    self.tableWidget_4.setSizeIncrement(QtCore.QSize(1181, 38))
                    self.tableWidget_4.insertRow(r)
                    for c,cd in enumerate(rd):
                        item = QtWidgets.QTableWidgetItem(str(cd))
                        if (c in [0,1,2,3,5,6,7]):
                            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                        self.tableWidget_4.setItem(r,c,item)
            self.tableWidget_4.resizeRowsToContents()

            self.lineEdit_14 = QtWidgets.QLineEdit(self.tab_2)
            self.lineEdit_14.setGeometry(QtCore.QRect(560, 34, 221, 31))
            self.lineEdit_14.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.lineEdit_14.setObjectName("lineEdit_14")
            self.label_19 = QtWidgets.QLabel(self.tab_2)
            self.label_19.setGeometry(QtCore.QRect(460, 40, 91, 21))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label_19.setFont(font)
            self.label_19.setObjectName("label_19")
            self.pushButton_6 = QtWidgets.QPushButton(self.tab_2)
            self.pushButton_6.setGeometry(QtCore.QRect(840, 35, 61, 30))
            self.pushButton_6.setStyleSheet("background-color: rgb(255, 170, 0);")
            self.pushButton_6.clicked.connect(self.tabulateSeller)
            self.pushButton_6.setObjectName("pushButton_6")
            self.pushButton_5 = QtWidgets.QPushButton(self.tab_2)
            self.pushButton_5.setGeometry(QtCore.QRect(790, 35, 41, 30))
            self.pushButton_5.setStyleSheet("background-color: rgb(255, 170, 0);")
            self.pushButton_5.clicked.connect(self.findSeller)
            self.pushButton_5.setObjectName("pushButton_5")
            self.pushButton_20 = QtWidgets.QPushButton(self.tab_2)
            self.pushButton_20.setGeometry(QtCore.QRect(690, 690, 93, 41))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_20.setFont(font)
            self.pushButton_20.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.pushButton_20.clicked.connect(self.cancelSeller)
            self.pushButton_20.setObjectName("pushButton_20")
            self.pushButton_21 = QtWidgets.QPushButton(self.tab_2)
            self.pushButton_21.setGeometry(QtCore.QRect(530, 690, 93, 41))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_21.setFont(font)
            self.pushButton_21.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.pushButton_21.clicked.connect(self.saveSeller)
            self.pushButton_21.setObjectName("pushButton_21")
            self.pushButton_22 = QtWidgets.QPushButton(self.tab_2)
            self.pushButton_22.setGeometry(QtCore.QRect(330, 690, 100, 41))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_22.setFont(font)
            self.pushButton_22.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.pushButton_22.clicked.connect(self.addSeller)
            self.pushButton_22.setObjectName("pushButton_20")
            self.pushButton_23 = QtWidgets.QPushButton(self.tab_2)
            self.pushButton_23.setGeometry(QtCore.QRect(850, 690, 125, 41))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_23.setFont(font)
            self.pushButton_23.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.pushButton_23.clicked.connect(self.deleteSeller)
            self.pushButton_23.setObjectName("pushButton_21")
            self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_3)
        self.tableWidget_2.setGeometry(QtCore.QRect(330, 160, 621, 401))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tableWidget_2.setFont(font)
        self.tableWidget_2.setAutoFillBackground(False)
        self.tableWidget_2.setStyleSheet("background-color: rgb(255, 170, 127);\n"
"border-color: rgb(0, 0, 0);")
        self.tableWidget_2.setLineWidth(1)
        self.tableWidget_2.setTabKeyNavigation(True)
        self.tableWidget_2.setWordWrap(True)
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setCornerButtonEnabled(True)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setMinimumSize(QtCore.QSize(621, 31))
        self.tableWidget_2.setMaximumSize(QtCore.QSize(621, 401))
        self.tableWidget_2.setSizeIncrement(QtCore.QSize(621, 38))
        self.tableWidget_2.setBaseSize(QtCore.QSize(621, 38))
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        self.tableWidget_2.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(200)
        self.tableWidget_2.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(False)

        db = MySQLdb.connect(host="localhost",user="root",passwd="")
        c=db.cursor()
        c.execute("use project")
        c.execute("select * from department")
        f = c.fetchall()
        for r,rd in enumerate(f):
            self.tableWidget_2.setSizeIncrement(QtCore.QSize(621, 38))
            self.tableWidget_2.insertRow(r)
            for c,cd in enumerate(rd):
                self.tableWidget_2.setItem(r,c,QtWidgets.QTableWidgetItem(str(cd)))
        self.tableWidget_2.resizeRowsToContents()

        self.label_5 = QtWidgets.QLabel(self.tab_3)
        self.label_5.setGeometry(QtCore.QRect(420, 56, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setGeometry(QtCore.QRect(520, 50, 221, 31))
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255); font-family: Segoe UI;")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_7.setGeometry(QtCore.QRect(800, 51, 61, 30))
        self.pushButton_7.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.pushButton_7.clicked.connect(self.tabulateDepartment)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_8.setGeometry(QtCore.QRect(750, 51, 41, 30))
        self.pushButton_8.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.pushButton_8.clicked.connect(self.findDepartment)
        self.pushButton_8.setObjectName("pushButton_8")
        self.tabWidget.addTab(self.tab_3, "")
        if self.department=="Purchase":
            self.tab_4 = QtWidgets.QWidget()
            self.tab_4.setObjectName("tab_4")
            self.lineEdit_3 = QtWidgets.QLineEdit(self.tab_4)
            self.lineEdit_3.setGeometry(QtCore.QRect(530, 30, 221, 31))
            self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.lineEdit_3.setObjectName("lineEdit_3")
            self.tableWidget_3 = QtWidgets.QTableWidget(self.tab_4)
            self.tableWidget_3.setGeometry(QtCore.QRect(205, 70, 891, 601))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            self.tableWidget_3.setFont(font)
            self.tableWidget_3.setStyleSheet("background-color: rgb(255, 170, 127);\n"
    "border-color: rgb(0, 0, 0);")
            self.tableWidget_3.setLineWidth(1)
            self.tableWidget_3.setTabKeyNavigation(True)
            self.tableWidget_3.setWordWrap(True)
            self.tableWidget_3.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tableWidget_3.setCornerButtonEnabled(True)
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.setColumnCount(6)
            self.tableWidget_3.setObjectName("tableWidget_3")
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
            c.execute("select b_s_id, b_date, b_Cattle_Type, b_Milk_Qty, b_Amount, b_e_id from bill where b_e_id = %s",[self.id])
            f = c.fetchall()
            for r,rd in enumerate(f):
                if rd[5]==self.id:
                    self.tableWidget_3.setSizeIncrement(QtCore.QSize(891, 38))
                    self.tableWidget_3.insertRow(r)
                    for c,cd in enumerate(rd):
                        item = QtWidgets.QTableWidgetItem(str(cd))
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
            self.pushButton_9 = QtWidgets.QPushButton(self.tab_4)
            self.pushButton_9.setGeometry(QtCore.QRect(810, 31, 61, 30))
            self.pushButton_9.setStyleSheet("background-color: rgb(255, 170, 0);")
            self.pushButton_9.clicked.connect(self.tabulateSale)
            self.pushButton_9.setObjectName("pushButton_9")
            self.pushButton_10 = QtWidgets.QPushButton(self.tab_4)
            self.pushButton_10.setGeometry(QtCore.QRect(760, 31, 41, 30))
            self.pushButton_10.setStyleSheet("background-color: rgb(255, 170, 0);")
            self.pushButton_10.clicked.connect(self.findSale)
            self.pushButton_10.setObjectName("pushButton_10")
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
        EmployeePage1.setCentralWidget(self.centralwidget)
        self.retranslateUi(EmployeePage1)
        self.tabWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(EmployeePage1)

    def retranslateUi(self, EmployeePage1):
        _translate = QtCore.QCoreApplication.translate
        EmployeePage1.setWindowTitle(_translate("EmployeePage1", "Employee Page"))
        self.label_2.setText(_translate("EmployeePage1", self.name))
        self.label_12.setText(_translate("EmployeePage1", "CHANGE PASSWORD :"))
        self.label_13.setText(_translate("EmployeePage1", "DETAILS :"))
        self.label_11.setText(_translate("EmployeePage1", "PH. NO."))
        self.label_24.setText(_translate("EmployeePage1", "RE-ENTER PASSWORD"))
        self.label_4.setText(_translate("EmployeePage1", "EMPLOYEE ID"))
        self.label_10.setText(_translate("EmployeePage1", "DATE OF BIRTH"))
        self.label_15.setText(_translate("EmployeePage1", "JOB TITLE"))
        self.label_9.setText(_translate("EmployeePage1", "DATE OF JOINING"))
        self.label_17.setText(_translate("EmployeePage1", "DEPARTMENT"))
        self.label_7.setText(_translate("EmployeePage1", "NAME"))
        self.label_18.setText(_translate("EmployeePage1", "GENDER"))
        self.label_22.setText(_translate("EmployeePage1", "USER ID"))
        self.label_14.setText(_translate("EmployeePage1", "ADMIN ID"))
        self.label_16.setText(_translate("EmployeePage1", "SALARY"))
        self.label_23.setText(_translate("EmployeePage1", "PASSWORD"))
        self.label_8.setText(_translate("EmployeePage1", "ADDRESS"))
        self.label_20.setText(_translate("EmployeePage1", "PROFILE PHOTO :"))
        self.pushButton_11.setText(_translate("EmployeePage1", "Click Here To Open The File Location"))
        self.pushButton_19.setText(_translate("EmployeePage1", "CANCEL"))
        self.pushButton_18.setText(_translate("EmployeePage1", "SAVE"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("EmployeePage1", "My Profile"))
        if self.department=="Purchase":
            item = self.tableWidget_4.horizontalHeaderItem(0)
            item.setText(_translate("EmployeePage1", "Seller ID"))
            item = self.tableWidget_4.horizontalHeaderItem(1)
            item.setText(_translate("EmployeePage1", "Name"))
            item = self.tableWidget_4.horizontalHeaderItem(2)
            item.setText(_translate("EmployeePage1", "User ID"))
            item = self.tableWidget_4.horizontalHeaderItem(3)
            item.setText(_translate("EmployeePage1", "Date of Birth"))
            item = self.tableWidget_4.horizontalHeaderItem(4)
            item.setText(_translate("EmployeePage1", "Salary"))
            item = self.tableWidget_4.horizontalHeaderItem(5)
            item.setText(_translate("EmployeePage1", "Employee ID"))
            item = self.tableWidget_4.horizontalHeaderItem(6)
            item.setText(_translate("EmployeePage1", "Phone No."))
            item = self.tableWidget_4.horizontalHeaderItem(7)
            item.setText(_translate("EmployeePage1", "Address"))
            self.label_19.setText(_translate("EmployeePage1", "SEARCH"))
            self.pushButton_6.setText(_translate("EmployeePage1", "Clear"))
            self.pushButton_5.setText(_translate("EmployeePage1", "Ok"))
            self.pushButton_20.setText(_translate("EmployeePage1", "CANCEL"))
            self.pushButton_21.setText(_translate("EmployeePage1", "SAVE"))
            self.pushButton_22.setText(_translate("EmployeePage1", "ADD SELLER"))
            self.pushButton_23.setText(_translate("EmployeePage1", "DELETE SELLER"))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("EmployeePage1", "Seller Details"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("EmployeePage1", "Department ID"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("EmployeePage1", "Department Name"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("EmployeePage1", "Admin ID"))
        self.label_5.setText(_translate("EmployeePage1", "SEARCH"))
        self.pushButton_7.setText(_translate("EmployeePage1", "Clear"))
        self.pushButton_8.setText(_translate("EmployeePage1", "Ok"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("EmployeePage1", "Department Details"))
        if self.department=="Purchase":
            item = self.tableWidget_3.horizontalHeaderItem(0)
            item.setText(_translate("EmployeePage1", "Seller ID"))
            item = self.tableWidget_3.horizontalHeaderItem(1)
            item.setText(_translate("EmployeePage1", "Date"))
            item = self.tableWidget_3.horizontalHeaderItem(2)
            item.setText(_translate("EmployeePage1", "Milk Quantity"))
            item = self.tableWidget_3.horizontalHeaderItem(3)
            item.setText(_translate("EmployeePage1", "Cattle Type"))
            item = self.tableWidget_3.horizontalHeaderItem(4)
            item.setText(_translate("EmployeePage1", "Price(per Ltrs)"))
            item = self.tableWidget_3.horizontalHeaderItem(5)
            item.setText(_translate("EmployeePage1", "Employee ID"))
            self.label_6.setText(_translate("EmployeePage1", "SEARCH"))
            self.pushButton_9.setText(_translate("EmployeePage1", "Clear"))
            self.pushButton_10.setText(_translate("EmployeePage1", "Ok"))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("EmployeePage1", "Purchase Report"))
        self.label_3.setText(_translate("EmployeePage1", "WELCOME"))
        self.pushButton_4.setText(_translate("EmployeePage1", "LOGOUT"))

import AdminR
import LogoR