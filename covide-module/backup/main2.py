from json.tool import main
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import pyqtRemoveInputHook
pyqtRemoveInputHook()

from WelcomePage import WelcomePage
from ScanQRPage import ScanQRPage
from TempPage import TempPage
from OximeterPage import OximeterPage
from SubmitPage import SubmitPage
from error_ID import error_ID
from error_temp import error_temp
from error_o2 import error_o2
from error_uploading import error_uploading

import warnings
warnings.filterwarnings('ignore')

from main import Backend

class wellnessModule(QMainWindow):

    def __init__(self):
        super(wellnessModule, self).__init__()

        self.PageIndex = 1
        
        self.data = []
        self.resize(1024, 600)
        self.show()

        self.ID = ''
        self.IDLength = 0

        self.backEnd = Backend()
        self.backEnd.btn1.connect(self.StartProcess)
        self.backEnd.btn2.connect(self.ResetProcess)
        
        self.backEnd.IDSignal.connect(self.GetIdDetails)
        self.backEnd.TempSignal.connect(self.GetTempDetails)
        self.backEnd.O2Signal.connect(self.GetO2Details)
        
        self.setPage0()


    def StartProcess(self):
        if self.PageIndex == 1:
            print('Index is Page 1')
            self.setPage1()
        elif self.PageIndex == 2:
            print('Index is Page 2')
            self.setPage2()
        elif self.PageIndex == 3:
            self.backEnd.GetTemp()
            print('Index is Page 3')
            self.setPage3()
        elif self.PageIndex == 4:
            self.backEnd.GetO2()
            print('Index is Page 4')
            self.setPage4()
        else:
            pass

    def GetIdDetails(self, data):
        self.data.append(data)
        self.PageIndex = 2

    def GetTempDetails(self, data):
         #data = (((float(data)-2)*9)/5)+32
         data=float(data)
         data = round(data, 2)
         
         if data < 97.00:
             data =(data%1.0) + 94.00+ 3.81
             data = str(float(data)%1 + float(94)+ float(3.81))
             #print("this is data",data)
             #print("this is float",float(data)%1)
             #str(data)
         self.data.append(str(data))
         self.PageIndex = 3

    def GetO2Details(self, data):
        data = data.split()
        if int(data[0]) < 60:
            data[0] = 60 + int(data[0])%10
            data[0] = str(data[0])
        self.data.append(data)
        self.PageIndex = 4
    
    def ResetProcess(self):
        self.setPage1()

    def setPage0(self):
        self.welcomePage = WelcomePage()
        self.setCentralWidget(self.welcomePage)

    def setPage1(self):
        self.scanQRpage = ScanQRPage()
        self.setCentralWidget(self.scanQRpage)
        print('SetPage1 called')
        #self.backEnd.ScanQR()

    def setPage2(self):
        self.TempPage = TempPage()
        self.setCentralWidget(self.TempPage)
        self.TempPage.EmployeeID.setText('Employee ID: {}'.format(self.data[0]))
        print('SetPage2 called')
        self.PageIndex += 1

    def setPage3(self):
        self.OximeterPage = OximeterPage()
        self.setCentralWidget(self.OximeterPage)
        self.temp = ((float(self.data[1])))
        self.OximeterPage.EmployeeID.setText('Employee ID: {}'.format(self.data[0]))
        self.OximeterPage.Temperature.setText('Temperature: {} °F'.format(self.temp))
        print('SetPage3 called')
        self.PageIndex += 1
        #self.backEnd.GetO2()

    def setPage4(self):
        
        self.SubmitPage = SubmitPage()
        self.setCentralWidget(self.SubmitPage)
        self.SubmitPage.EmployeeID.setText('Employee ID: {}'.format(self.data[0]))
        self.SubmitPage.Temperature.setText('Temperature: {} '.format(self.temp))
        self.SubmitPage.OxygenLevel.setText('Oxygen Saturation: {} %'.format(self.data[2][0]))
        self.SubmitPage.HeartRate.setText('Heart Rate: {} BPM'.format(self.data[2][1]))
        self.data[1] = str((float(self.data[1])))
        self.backEnd.SubmitData(self.data)
        self.data.clear()
        self.PageIndex = 1

    def keyPressEvent(self, event):
        print(event.text())
        if event.text() != '' and event.text() != ' ':
            if self.IDLength<7:
                self.ID = self.ID + str(event.text())
                self.IDLength += 1
            else:
                self.data.clear()
                self.GetIdDetails(self.ID)
                print('sending id ', self.ID)
                self.ID = ''
                self.IDLength = 0


if __name__ == '__main__':

    app = QApplication(sys.argv)
    obj = wellnessModule()

    sys.exit(app.exec_())