import serialCom


print(serialCom.getSerialPorts())

# TS:   Temperatura configurada em °C
# TR:   Temperatura real no momento da leitura em °C
# HM:   Umidade lida em %
# FAN:  Velocidade do FAN em %
# ALM1: Alarme 01 em HH:MM:SS
# ALM1: Alarme 02 em HH:MM:SS
# RTC:  Horário do RTC em HH:MM:SS
# PI:   Ganhos do controlador PI [Kp:Ki] (para debug)

msgSample = '''
>TS:39.5\n
>TR:38.3\n
>HM:30.4\n
>FAN:50\n
>ALM1:10:00:00\n
>ALM2:18:00:00\n
>RTC:12:25:45\n
>PI:2.3:5.1\n
'''

serialCom.initSerialCom()

data = serialCom.dataParse(msgSample)

print (data)

print (data['PI'][0])