import serial
import serial.tools.list_ports
import re

expressoesRegulares = list()

regexList = [
    r'>(TS):(\d{1,2}.\d{1})',
    r'>(TR):(\d{1,2}.\d{1})',
    r'>(HM):(\d{1,2}.\d{1})',
    r'>(FAN):(\d{1,2})',    
    r'>(ALM1):(\d{1,2}:\d{1,2}:\d{1,2})',     
    r'>(ALM2):(\d{1,2}:\d{1,2}:\d{1,2})',     
    r'>(RTC):(\d{1,2}:\d{1,2}:\d{1,2})',
    r'>(PI):(\d{1,3}.{1,2}):(\d{1,3}.{1,2})'
]

def getSerialPorts() :
    ports = [p.device for p in serial.tools.list_ports.comports()]
    return ports

def initSerialCom () :
    # Generate Regex List
    for rgx in regexList:
        expressoesRegulares.append(re.compile(rgx))


def dataParse(msg):
    msgList = msg.split()
    checkedVals = dict()

    if len(msgList) != len(expressoesRegulares):
        return -1
    
    for i in range(len(msgList)):
        reSearch = expressoesRegulares[i].search(msgList[i])
        if reSearch :
            if reSearch.group(1) == 'PI' :
                checkedVals[reSearch.group(1)] = [reSearch.group(2), reSearch.group(3)]
            else :
                checkedVals[reSearch.group(1)] = reSearch.group(2)
        else :
            return -1
    
    return checkedVals