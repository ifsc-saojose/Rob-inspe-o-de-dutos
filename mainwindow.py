# -*- coding: utf-8 -*-

import PyQt4.QtGui as GUI
import PyQt4.QtCore as QtCore
import Actions
import Config_window
import cv
import time
from PyQt4 import uic

(Ui_MainWindow, QMainWindow) = uic.loadUiType('GUI/mainwindow.ui')


class MainWindow(QMainWindow):
    """MainWindow inherits QMainWindow"""

    _timer = QtCore.QTimer
    _ports = []
    _baud_rate = ["4800", "9600", "19200", "38400", "57600", "115200"]
    _configuration_window = None
    #_fourcc = cv2.VideoWriter_fourcc(*'XVID')
    _writer = None

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.Set_Size_itens()
        self.ui.Close_Button.clicked.connect(self.Close_Button_Clicked)
        self.ui.OK_Button.clicked.connect(self.OK_Button_Clicked)
        self.ui.Refresh_Button.clicked.connect(self.Refresh_Button_Clicked)
        self.ui.Record_Button.clicked.connect(self.Record_Button_Clicked)
        self.ui.Config_Button.clicked.connect(self.Config_Button_Clicked)
        self.ui.Close_Button.setEnabled(False)
        self.SpeedLCD_Display(50)
        self._ports = Actions.serial_ports()
        self.ui.comboBox_Port.addItems(self._ports)
        self.ui.comboBox_Baud.addItems(self._baud_rate)
        Actions.Set_Address()
        self.Cam_Loop()

    def Cam_Loop(self):
        try:
            self.Cam_Video()
        finally:
            self._timer.singleShot(150, self.Cam_Loop)

    def Serial_Loop(self):
        if(Actions._porta_serial.isOpen()):
            try:
                print("")
                #value = Actions.Serial_Read()
                #Actions.comand_decipher(value)

            finally:
                self._timer.singleShot(100, self.Serial_Loop)

    def Set_Size_itens(self):
        #self.ui.Label_Image.setMinimumSize(640, 480)
        self.ui.Record_Button.setMaximumSize(100, 25)
        #self.ui.OK_Button.setMaximumSize(50, 25)
        self.ui.comboBox_Port.setMaximumSize(260, 25)
        #self.ui.comboBox_Port.setMinimumSize(260, 25)
        self.ui.Port_Label.setMaximumHeight(40)
        #elf.ui.Port_Label.setMinimumHeight(40)
        #self.ui.Speed_Label.setMinimumHeight(40)
        self.ui.Speed_Label.setMaximumHeight(40)
        #self.ui.SpeedLCD.setMinimumHeight(40)
        self.ui.SpeedLCD.setMaximumHeight(40)

    def Config_Button_Clicked(self):
        if(self._configuration_window is None):
            #self.ui.Config_Button.setEnabled(False)
            self._configuration_window = Config_window.Config_window(self)
            self._configuration_window.show()
            self._configuration_window.setWindowTitle('Configurations')
            self._configuration_window.exec_()
            self._configuration_window = None

    def Close_Button_Clicked(self):
        Actions._porta_serial.close()
        self.ui.Close_Button.setEnabled(False)
        self.ui.OK_Button.setEnabled(True)

    def OK_Button_Clicked(self):
        Actions.Serial_Open(str(self.ui.comboBox_Port.currentText()),
        int(self.ui.comboBox_Baud.currentText()))
        self.ui.Close_Button.setEnabled(True)
        self.ui.OK_Button.setEnabled(False)
        self.Serial_Loop()

    def Refresh_Button_Clicked(self):
        for i in range(0, len(self._ports)):
            self.ui.comboBox_Port.removeItem(i)

        self._ports = Actions.serial_ports()
        self.ui.comboBox_Port.addItems(self._ports)

    def Record_Button_Clicked(self):
        if(not self.ui.Record_Button.isFlat()):
            self.ui.Record_Button.setText("Parar")
            self.ui.Record_Button.setFlat(True)
            self._writer = cv.CreateVideoWriter(
         filename=("img/" + time.strftime("%H%M%S") + ".avi"),
         fourcc=cv.CV_FOURCC('X', 'V', 'I', 'D'),
         fps=2,
         frame_size=(640, 480),
         is_color=1)
        else:
            self.ui.Record_Button.setText("Gravar")
            self.ui.Record_Button.setFlat(False)
            cv.ReleaseVideoWriter(self._writer)

    def SpeedLCD_Display(self, increment):
        value = self.ui.SpeedLCD.intValue() + increment
        self.ui.SpeedLCD.display(value)

    def Image_Show(self, filename):
        # Carrega uma imagen na tela
        pixmap = GUI.QPixmap(filename)
        self.ui.Label_Image.setPixmap(pixmap)
        self.ui.Label_Image.show()

    def Cam_Video(self):
        # Recebe uma imagem e manda mostrar na tela
        Actions.Receive_File()
        if(self.ui.Record_Button.isFlat()):
            frame = cv.LoadImage("img/img.jpg")
            cv.WriteFrame(self._writer, frame)
        self.Image_Show("img/img.jpg")

    def __del__(self):
        self.ui = None
