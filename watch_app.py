import serial
import time
import glob
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic, QtSerialPort, QtCore

class MyGUI(QMainWindow):    
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("watch_gui.ui", self)
        self.show()
        self.pushButton.clicked.connect(self.refresh)
        self.pushButton_2.clicked.connect(self.connect)
        
    def ports(self):
    #   if sys.platform.startwith('win'):
        ports = ['COM%s' % (i+1) for i in range(256)]  
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def refresh(self):
        self.serial_port_list = self.ports()
        self.comboBox.clear()
        self.comboBox.addItems( self.serial_port_list)
        
    def connect(self):
        if self.pushButton_2.isChecked():
            self.chosen_serial_port = self.comboBox.currentText()
            self.serial =  QtSerialPort.QSerialPort(
                self.chosen_serial_port,
                baudRate=QtSerialPort.QSerialPort.Baud9600,
                readyRead = self.receive        
            )
            if not self.serial.isOpen():
                if not self.serial.open(QtCore.QIODevice.ReadWrite):
                    self.pushButton_2.setChecked(False)
        else:
            self.serial.close()

    def receive(self):
        pass

def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == "__main__":
    main()