# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import speech_recognition as sr
import os
import threading

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.inpAdd = QtWidgets.QLineEdit(self.centralwidget)
        self.inpAdd.setGeometry(QtCore.QRect(70, 60, 661, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.inpAdd.setFont(font)
        self.inpAdd.setText("")
        self.inpAdd.setObjectName("inpAdd")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(70, 20, 471, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label1.setFont(font)
        self.label1.setObjectName("label1")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 160, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.OpText = QtWidgets.QTextEdit(self.centralwidget)
        self.OpText.setGeometry(QtCore.QRect(70, 180, 661, 351))
        self.OpText.setObjectName("OpText")
        self.OpText.setReadOnly(True)
        self.submitbut = QtWidgets.QPushButton(self.centralwidget)
        self.submitbut.setGeometry(QtCore.QRect(70, 110, 93, 28))
        self.submitbut.setObjectName("submitbut")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label1.setText(_translate("MainWindow", "Path of Directory containing Audio Resumes :"))
        self.label.setText(_translate("MainWindow", "OUTPUT :"))
        self.submitbut.setText(_translate("MainWindow", "Submit"))
        self.submitbut.clicked.connect(self.submit)
    
    def getoutput(self, path):
        dictf=r"..\words_alpha.txt"
        os.chdir(path)
        flist=os.listdir()
        reslist=[]
        wrds=[]        #list of words in the file
        acc=0
        
        def wordInFile(wrd):
            dic=open(dictf)
            for dw in dic:
                if(dw[:-1]==wrd):
                    return True
            return False
        
        for file in flist:
            if(file[-4:]=='.wav'):
                self.OpText.append('processing : '+file)
                print('processing : '+file)
                audio_file=(file)
                fpth=file[:-4]+'.txt'
                reslist.append(fpth)
                fo=open(fpth,'wt')
                r=sr.Recognizer()
                with sr.AudioFile(audio_file) as source:
                    #reads the audio file.Here we use record instead of listen
                    audio = r.record(source)
                try:
                    #print('The audio contains : '+r.recognize_google(audio))
                    fo.write(r.recognize_google(audio))
                    fo.close()
        
                except sr.UnknownValueError:
                    self.OpText.append('Google Speech Recognition could not understand audio')
                    print('Google Speech Recognition could not understand audio')
        
                except sr.RequestError as e:
                    self.OpText.append('Could not request result from google speech recognition service; {0}'.format(e))
                    print('Could not request result from google speech recognition service; {0}'.format(e))
        
        
        #now read word by word from each file in reslist and compare these words in dictionary.
        for fl in reslist:
            wrds=[]
            fo=open(fl)
            acc=0
            for line in fo:
                wrds.extend(line.split(' '))    #list of words in the file
            for wd in wrds:
                if wordInFile(wd):
                    acc+=1
            accuracy=(acc/len(wrds))*100
            self.OpText.append("The english accuracy of "+fl[:-4]+" is : "+str(accuracy)+"%")
            print("The english accuracy of "+fl[:-4]+" is : "+str(accuracy)+"%")
        self.OpText.append("-----------------Thanks for using this software-------------------")
    
    def submit(self):
        path = self.inpAdd.text()
        output = threading.Thread(target = self.getoutput, args=(path,))
        output.start()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

