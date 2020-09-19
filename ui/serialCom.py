import serial
import serial.tools.list_ports


def getSerialPorts() :
    ports = [p.device for p in serial.tools.list_ports.comports()]
    return ports