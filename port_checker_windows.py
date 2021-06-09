import serial
import time


##################################################################################################################
############################# This code check which ports are available and work. ################################
######################################## Apply only for Windows OS. ##############################################
##################################################################################################################
list=['COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','COM10','COM11','COM12','COM13','COM14','COM15','COM16','COM17','COM18',]



COM1='COM1'
COM2='COM2'
COM3='COM3'
COM4='COM4'
COM5='COM5'
COM6='COM6'
COM7='COM7'
COM8='COM8'
COM9='COM9'
COM10='COM10'
COM11='COM11'
COM12='COM12'
COM13='COM13'
COM14='COM14'
COM15='COM15'
COM16='COM16'
COM17='COM17'
COM18='COM18'
COM19='COM19'
time.sleep(1)
ser = serial.Serial()

ser.baudrate = 9600

i=1

while True:
    time.sleep(.2)
    print(i)
    ser.port = list[i]
    try:

        ser.open()
        if ser.isOpen()==True:
            print('connected')
            #print('arduino is on COMPORT'.join(i))
            break
        break

    except:
        print('waiting')
        i=i+1
        if i==18:
            print('Kindly remove usb cable and try again')
            break


print('here we go')
while True:
    print(ser.readline())
