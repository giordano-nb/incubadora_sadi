import serialCom
from PyQt5 import QtWidgets, uic
import sys

# TS:   Temperatura configurada em °C
# TR:   Temperatura real no momento da leitura em °C
# HM:   Umidade lida em %
# FAN:  Velocidade do FAN em %
# ALM1: Alarme 01 em HH:MM:SS
# ALM1: Alarme 02 em HH:MM:SS
# RTC:  Horário do RTC em HH:MM:SS
# PI:   Ganhos do controlador PI [Kp:Ki] (para debug)

# msgSample = '''
# >TS:39.5\n
# >TR:38.3\n
# >HM:30.4\n
# >FAN:50\n
# >ALM1:10:00:00\n
# >ALM2:18:00:00\n
# >RTC:12:25:45\n
# >PI:2.3:5.1\n
# '''

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Chocadeira_UI.ui', self)

        self.button = self.findChild(QtWidgets.QPushButton, 'redefinir') # Find the button
        self.button.clicked.connect(self.redefinirButtonPressed) # Remember to pass the definition/method, not the return value!
        self.input = self.findChild(QtWidgets.QLineEdit, 'tempRef')
        self.show()

    def redefinirButtonPressed(self):
        # This is executed when the button is pressed
        print('redefinirButtonPressed'+' TempRef: '+self.input.text())

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

# print(serialCom.getSerialPorts())

# serialCom.initSerialCom('COM3')

# msg = serialCom.readDataFromSerial()

# data = serialCom.dataParse(msg)

# print (data)

# print (data['PI'][0])