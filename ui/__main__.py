import serialCom
import sys, time
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
import traceback, sys


serialCom.initSerialCom('COM3')


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Chocadeira_UI.ui', self)
        
        self.quitThread = False

        self.redefinirButton = self.findChild(QtWidgets.QPushButton, 'redefinir')
        self.confirmarButton = self.findChild(QtWidgets.QPushButton, 'confirmar')

        self.confirmarButton.clicked.connect(self.confirmarButtonPressed) # Remember to pass the definition/method, not the return value!

        self.tempRefTextBox = self.findChild(QtWidgets.QDoubleSpinBox, 'tempRef')
        self.fanSpeedTextBox = self.findChild(QtWidgets.QDoubleSpinBox, 'fanSpeed')
        self.periodoAlertaTimeEdit = self.findChild(QtWidgets.QTimeEdit, 'periodoAlerta')

        self.tempAmbInfo = self.findChild(QtWidgets.QLineEdit, 'tempAmbInfo')
        self.tempRefInfo = self.findChild(QtWidgets.QLineEdit, 'tempRefInfo')
        self.FanSpeedInfo = self.findChild(QtWidgets.QLineEdit, 'FanSpeedInfo')
        self.umidadeInfo = self.findChild(QtWidgets.QLineEdit, 'umidadeInfo')
        self.periodoAlertaInfo = self.findChild(QtWidgets.QTimeEdit, 'periodoAlertaInfo')
        self.rtcTime = self.findChild(QtWidgets.QTimeEdit, 'rtcTime')

        self.show()

        self.threadpool = QThreadPool()
        self.threadpool.start(self.updateVals) 

    def confirmarButtonPressed(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Valores digitados")
        msg.setText("tempRef = {} \nfanSpeed = {} \nperiodoAlerta= {} \n".format(
                    self.tempRefTextBox.text(), 
                    self.fanSpeedTextBox.text(), 
                    self.periodoAlertaTimeEdit.text())
        )
        msg.exec_()
    

    def updateVals (self):
        while not self.quitThread :
            time.sleep(1)
            msg = serialCom.readDataFromSerial()
            data = serialCom.dataParse(msg)
            if data:
                try:
                    self.tempAmbInfo.setText(data['TR'])
                    self.tempRefInfo.setText(data['TS'])
                    self.FanSpeedInfo.setText(data['FAN'])
                    self.umidadeInfo.setText(data['HM'])
                    self.periodoAlertaInfo.setTime(QTime.fromString(data['ALM1']))
                    self.rtcTime.setTime(QTime.fromString(data['RTC']))
                except:
                    continue
        return 0

    def myExitHandler (self):
        self.quitThread = True

app = QtWidgets.QApplication(sys.argv)

window = Ui()
app.aboutToQuit.connect(window.myExitHandler)
app.exec_()