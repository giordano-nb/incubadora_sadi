import serialCom
import sys, time
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
import traceback, sys
from datetime import datetime


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Chocadeira_UI.ui', self)
        
        self.configuredSerial = False
        self.quitThread = False

        self.redefinirButton = self.findChild(QtWidgets.QPushButton, 'redefinir')
        self.confirmarButton = self.findChild(QtWidgets.QPushButton, 'confirmar')
        self.connectarButton = self.findChild(QtWidgets.QPushButton, 'connectarButton')

        self.confirmarButton.clicked.connect(self.confirmarButtonPressed)

        self.connectarButton.clicked.connect(self.changeSerialPort)
        self.redefinirButton.clicked.connect(self.redefinirConfigs)

        self.tempRefTextBox = self.findChild(QtWidgets.QDoubleSpinBox, 'tempRef')
        self.fanSpeedTextBox = self.findChild(QtWidgets.QDoubleSpinBox, 'fanSpeed')
        self.periodoAlertaTimeEdit = self.findChild(QtWidgets.QTimeEdit, 'periodoAlerta')

        self.tempAmbInfo = self.findChild(QtWidgets.QLineEdit, 'tempAmbInfo')
        self.tempRefInfo = self.findChild(QtWidgets.QLineEdit, 'tempRefInfo')
        self.FanSpeedInfo = self.findChild(QtWidgets.QLineEdit, 'FanSpeedInfo')
        self.umidadeInfo = self.findChild(QtWidgets.QLineEdit, 'umidadeInfo')
        self.periodoAlertaInfo = self.findChild(QtWidgets.QTimeEdit, 'periodoAlertaInfo')
        self.rtcTime = self.findChild(QtWidgets.QTimeEdit, 'rtcTime')
        self.rtcUpdate = self.findChild(QtWidgets.QCheckBox, 'rtcUpdate')
        self.serialPort = self.findChild(QtWidgets.QComboBox, 'serialPort')

        for port in serialCom.getSerialPorts():
            self.serialPort.addItem(port)

        
        self.show()

        self.threadpool = QThreadPool()
        self.threadpool.start(self.updateVals) 
        
    def redefinirConfigs(self) :
        self.configuredSerial = False
        time.sleep(1)
        serialCom.closeSerialCom()


    def changeSerialPort(self) :
        serialCom.initSerialCom(self.serialPort.currentText())
        time.sleep(1)
        self.configuredSerial = True


    def confirmarButtonPressed(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Valores digitados")
        
        RTC = datetime.now().strftime("%H:%M:%S") if self.rtcUpdate.checkState() else 'no'

        strToUpdate = '>TS:{}\n>FAN:{}\n>ALM1:{}\n>RTC:{}\n>PI:{}:{}\n'.format(self.tempRefTextBox.text(), 
                self.fanSpeedTextBox.text(), 
                self.periodoAlertaTimeEdit.text(), 
                RTC,
                2.5, 2.4
            )
        serialCom.sendDataToSerial(strToUpdate)
        msg.setText(strToUpdate)
        msg.exec_()
    

    def updateVals (self):
        while not self.quitThread :

            if not self.configuredSerial :
                continue

            time.sleep(1)

            try:
                msg = serialCom.readDataFromSerial()
                data = serialCom.dataParse(msg)
                if data:
                        self.tempAmbInfo.setText(data['TR'])
                        self.tempRefInfo.setText(data['TS'])
                        self.FanSpeedInfo.setText(data['FAN'])
                        self.umidadeInfo.setText(data['HM'])
                        self.periodoAlertaInfo.setTime(QTime.fromString(data['ALM1']))
                        self.rtcTime.setTime(QTime.fromString(data['RTC']))
            except Exception as err:
                print(err)
                continue
        return 0

    def myExitHandler (self):
        self.quitThread = True


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.aboutToQuit.connect(window.myExitHandler)
app.exec_()