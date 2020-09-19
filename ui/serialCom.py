import serial
import serial.tools.list_ports
import re

expressoesRegulares = list()
portaSerial = 0

# TS:   Temperatura configurada em °C
# TR:   Temperatura real no momento da leitura em °C
# HM:   Umidade lida em %
# FAN:  Velocidade do FAN em %
# ALM1: Alarme 01 em HH:MM:SS
# ALM1: Alarme 02 em HH:MM:SS
# RTC:  Horário do RTC em HH:MM:SS
# PI:   Ganhos do controlador PI [Kp:Ki] (para debug)


regexList = [
    r'>(TS):(\d{1,2}.\d{1,2})[\n\r]*$',
    r'>(TR):(\d{1,2}.\d{1,2})[\n\r]*$',
    r'>(HM):(\d{1,2}.\d{1,2})[\n\r]*$',
    r'>(FAN):(\d{1,2})[\n\r]*$',    
    r'>(ALM1):(\d{1,2}:\d{1,2}:\d{1,2})[\n\r]*$',
    r'>(ALM2):(\d{1,2}:\d{1,2}:\d{1,2})[\n\r]*$',     
    r'>(RTC):(\d{1,2}:\d{1,2}:\d{1,2})[\n\r]*$',
    r'>(PI):(\d{1,3}.{1,2}):(\d{1,3}.{1,2})[\n\r]*$'
]



def getSerialPorts () :
    ports = [p.device for p in serial.tools.list_ports.comports()]
    return ports



def initSerialCom (serialDevice) :
    global portaSerial, expressoesRegulares

    portaSerial = serial.Serial(serialDevice, 9600, timeout=3)
    for rgx in regexList:
        expressoesRegulares.append(re.compile(rgx))



def closeSerialCom (serialDevice) :
    global portaSerial 

    portaSerial.close()



def readDataFromSerial () :
    rectMsg = list()

    portaSerial.write(b's')
    portaSerial.flushInput()
    for _ in range(len(expressoesRegulares)) :
        try:
            rectMsg.append( portaSerial.readline().decode() )
        except Exception as err:
            print (err)
            return 0
    return rectMsg



def dataParse (msgList) :
    checkedVals = dict()

    if len(msgList) != len(expressoesRegulares):
        return 0
    
    for i in range(len(msgList)):
        reSearch = expressoesRegulares[i].search(msgList[i])
        if reSearch :
            if reSearch.group(1) == 'PI' :
                checkedVals[reSearch.group(1)] = [reSearch.group(2), reSearch.group(3)]
            else :
                checkedVals[reSearch.group(1)] = reSearch.group(2)
        else :
            return 0
    
    return checkedVals
