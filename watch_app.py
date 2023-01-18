import serial
import time
import glob
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QTime
from PyQt5 import uic, QtSerialPort, QtCore

class MyGUI(QMainWindow):    
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("watch_gui.ui", self)
        self.calendarWidget.showToday()
        self.timeEdit.setTime(QTime.currentTime())
        self.Time_to_Set.setTime(QTime.currentTime())
        self.show()
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.pushButton.clicked.connect(self.refresh)
        self.pushButton_2.clicked.connect(self.connect)
        self.Modify_Time.clicked.connect(self.modify_time)
        self.Set_Time.clicked.connect(self.set_time)
       
    def update_time(self):
        self.timeEdit.setTime(QTime.currentTime())
        if not self.Modify_Time.isChecked():
            self.Time_to_Set.setTime(QTime.currentTime())
    
    def set_time(self):
        if self.Set_Time.isChecked():
            time = self.Time_to_Set.time()
            time_string = time.toString()
            print(time_string)
            header = bytearray("SET\n","ASCII")
        #    time = bytearray(time_string,"ASCII")
            self.serial_comunication.write(header)
    
    def modify_time(self):
        if self.Modify_Time.isChecked():
            self.Time_to_Set.setEnabled(True)
        else:
            self.Time_to_Set.setEnabled(False)
        
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
            self.toggle(True)
            self.textEdit.clear()
            self.chosen_serial_port = self.comboBox.currentText()
            self.serial_comunication =  QtSerialPort.QSerialPort(
                self.chosen_serial_port,
                baudRate=QtSerialPort.QSerialPort.Baud9600,
                readyRead = self.receive        
            )
            if not self.serial_comunication.isOpen():
                if not self.serial_comunication.open(QtCore.QIODevice.ReadWrite):
                    self.pushButton_2.setChecked(False)
        else:
            self.serial_comunication.close()
            self.toggle(False)
            
    def toggle(self, state):
        self.textEdit.setEnabled(state)
        self.Check_Time.setEnabled(state)
        self.Set_Time.setEnabled(state)
        self.Check_Error.setEnabled(state)
            
    def receive(self):
        while self.serial_comunication.canReadLine():
            text = self.serial_comunication.readLine().data().decode()
            text = text.strip('\r\n')
            self.textEdit.append(text)

def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == "__main__":
    main()