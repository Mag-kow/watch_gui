import serial
import time
import sys 
import glob
from PyQt5.QtWidgets import *
from PyQt5 import uic


# def ports():
#  #   if sys.platform.startwith('win'):
#     ports = ['COM%s' % (i+1) for i in range(256)]
   
#     # result = []

    # for port in ports:
    #     try:
    #         s = serial.Serial(port)
    #         s.close()
    #         result.append(port)
    #     except (OSError, serial.SerialException)
    #         pass
    # return result

def main():
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM4'
    print(ser)
    ser.open()
    
    while(1):
      print(ser.readline())
      #  data = bytes("10:11:12",'utf-8')
        #data = bytearray("10:11:12","ASCII")
      data = bytearray("SET\n","ASCII")
       # data = 250
       # print(data)
      ser.write(data)
      time.sleep(2)
        




if __name__ == "__main__":
    main()