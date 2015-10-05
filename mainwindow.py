# -*- coding: utf-8 -*-

import PyQt4.QtGui as GUI
import PyQt4.QtCore as QtCore
import Actions
import Config_window
import cv
import time
import simplejson
import joystick
import socket
from PyQt4 import uic

(Ui_MainWindow, QMainWindow) = uic.loadUiType('GUI/mainwindow.ui')


class MainWindow(QMainWindow):
    """MainWindow inherits QMainWindow"""

    _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _packet = [4, 4, 4]
    _speed = 50
    _state = 0
    _timer = QtCore.QTimer
    _configuration_window = None
    _joystick = joystick.joystick()
    _writer = None

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Record_Button.clicked.connect(self.Record_Button_Clicked)
        self.ui.Config_Button.clicked.connect(self.Config_Button_Clicked)
        self.SpeedLCD_Display(self._speed)
        self.load_Configs()
        Actions.Set_Address()
        self.Cam_Loop()

    def Cam_Loop(self):
        try:
            #self.Cam_Video()
            try:
                self._packet = self.joystic_interpreter(
                    self._joystick.reading())
            except:
                self._packet = [4, 4, 4]
            data = simplejson.dumps(self._packet)
            self._sock.sendto(data, ("172.18.131.50", 5506))

        finally:
            self._timer.singleShot(50, self.Cam_Loop)

    def joystic_interpreter(self, key):

        data = [4, 4, self._speed]

        if(key[1] < 0):
            data[0] = 0

        elif(key[1] > 0):
            data[0] = 1

        elif (key[0] > 0):
            data[0] = 2

        elif(key[0] < 0):
            data[0] = 3

        if(key[3] < 0):
            data[1] = 0

        elif(key[3] > 0):
            data[1] = 1

        elif (key[2] > 0):
            data[1] = 2

        elif(key[2] < 0):
            data[1] = 3

        if(key[5] == 1):
            if(self._speed <= 99):
                self._speed += 1
                self.SpeedLCD_Display(self._speed)
                data[2] = self._speed

        elif (key[4] == 1):
            if(self._speed >= 2):
                self._speed -= 1
                self.SpeedLCD_Display(self._speed)
                data[2] = self._speed

        elif(key[6] == 1 and key[6] != self._state):
            self._state = 1
            self.Record_Button_Clicked()

        elif(key[6] == 0):
            self._state = 0

        return data

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

    def SpeedLCD_Display(self, value):
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

    def keyPressEvent(self, event):
        text = ""
        key = event.key()

        # Verifica se o botão pressionado é uma das teclas especias abaixo e
        # grava na variavel texto uma string descrevendo a tecla, caso contrio
        # grava o character que representa a tecla

        if(key == QtCore.Qt.Key_Left):
            text = "Left Arrow"

        elif key == QtCore.Qt.Key_Right:
            text = "Right Arrow"

        elif key == QtCore.Qt.Key_Down:
            text = "Down Arrow"

        elif key == QtCore.Qt.Key_Up:
            text = "Up Arrow"

        elif key == QtCore.Qt.Key_Space:
            text = "Space"

        elif key == QtCore.Qt.Key_Control:
            text = "Ctrl"

        elif key == QtCore.Qt.Key_Alt:
            text = "Alt"

        elif key == QtCore.Qt.Key_Return:
            text = "Return"

        elif key == QtCore.Qt.Key_Enter:
            text = "Enter"

        elif key == QtCore.Qt.Key_Shift:
            text = "Shift"

        elif key == QtCore.Qt.Key_AltGr:
            text = "AltGr"

        else:
            text = event.text()

        self.comand(text, 0)

    def comand(self, key, option):
        if(option == 0):
            comands = self._typesetter_config_options
        else:
            comands = self._control_config_options

        self._packet = [4, 4, self._speed]
        for i in range(0, 3):
            possibilits = comands[i]
            for a in range(0, len(possibilits)):
                if (key == possibilits[str(a)]):
                    if(i == 2 and a == 0):
                        if(self._speed <= 99):
                            self._speed = self._speed + 1
                            self.SpeedLCD_Display(self._speed)
                            self._packet[i] = self._speed

                    elif(i == 2 and a == 1):
                        if(self._speed >= 2):
                            self._speed = self._speed - 1
                            self.SpeedLCD_Display(self._speed)
                            self._packet[i] = self._speed

                    elif(i == 2 and a == 2):
                        self.Record_Button_Clicked()
                        break

                    else:
                        self._packet[i] = a

                    i = 3
                    break

        print((self._packet[0], self._packet[1], self._packet[2]))
        data = simplejson.dumps(self._packet)
        self._sock.sendto(data, ("172.18.131.23", 5506))

    def load_Configs(self):
        # Lê as configurações dos arquivos e grava em duas listas
        self._control_config_options = []
        self._typesetter_config_options = []

        config_file = open('configurations/control_config.txt', 'r')
        text_lines = [line.rstrip('\n') for line in config_file]

        for i in range(0, len(text_lines)):
            self._control_config_options.append(simplejson.loads(text_lines[i]))

        config_file.close()

        config_file = open('configurations/typesetter_config.txt', 'r')
        text_lines = [line.rstrip('\n') for line in config_file]
        for i in range(0, len(text_lines)):
            self._typesetter_config_options.append(
                simplejson.loads(text_lines[i]))

        config_file.close()

    def __del__(self):
        self.ui = None
