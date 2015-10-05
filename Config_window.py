# -*- coding: utf-8 -*-
import PyQt4.QtGui as Gui
import PyQt4.QtCore as Core
#import Actions
import simplejson
import pygame
from PyQt4 import uic

pygame.init()
(Ui_ConfigWindow, QConfigWindow) = uic.loadUiType('GUI/Config_Window.ui')


class Config_window(QConfigWindow):
    _control_config_options = []
    _typesetter_config_options = []

    def __init__(self, parent=None):
        QConfigWindow.__init__(self, parent)
        self.ui = Ui_ConfigWindow()
        self.ui.setupUi(self)
        #self.ui.MR_Control_ComboBox.currentIndexChanged.connect(self.MR_Control_Refresh)
        #self.ui.MC_Control_ComboBox.currentIndexChanged.connect(self.MC_Control_Refresh)
        #self.ui.Others_Control_ComboBox.currentIndexChanged.connect(self.Others_Control_Refresh)
        #self.ui.MR_Control_Button.clicked.connect(self.MR_Control_Config)
        #self.ui.MC_Control_Button.clicked.connect(self.MC_Control_Config)
        #self.ui.Others_Control_Button.clicked.connect(self.Others_Control_Config)
        self.ui.MR_TypeSetter_ComboBox.currentIndexChanged.connect(self.MR_TypeSetter_Refresh)
        self.ui.MC_TypeSetter_ComboBox.currentIndexChanged.connect(self.MC_TypeSetter_Refresh)
        self.ui.Others_TypeSetter_ComboBox.currentIndexChanged.connect(self.Others_TypeSetter_Refresh)
        self.ui.MR_TypeSetter_Button.clicked.connect(self.MR_TypeSetter_Config)
        self.ui.MC_TypeSetter_Button.clicked.connect(self.MC_TypeSetter_Config)
        self.ui.Others_TypeSetter_Button.clicked.connect(self.Others_TypeSetter_Config)
        #self.ui.Control_ButtonBox.button(Gui.QDialogButtonBox.Cancel).clicked.connect(self.close)
        #self.ui.Control_ButtonBox.button(Gui.QDialogButtonBox.Save).clicked.connect(self.control_Save_Configs)
        self.ui.TypeSetter_ButtonBox.button(Gui.QDialogButtonBox.Cancel).clicked.connect(self.close)
        self.ui.TypeSetter_ButtonBox.button(Gui.QDialogButtonBox.Save).clicked.connect(self.typesetter_Save_Configs)
        self.load_Configs()
        #self.MR_Control_Refresh()
        self.MR_TypeSetter_Refresh()
        #self.MC_Control_Refresh()
        self.MC_TypeSetter_Refresh()
        #self.Others_Control_Refresh()
        self.Others_TypeSetter_Refresh()
        self.ui.label.setFocus(True)

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
            self._typesetter_config_options.append(simplejson.loads(text_lines[i]))

        config_file.close()


# As funções abaixo atualizão o texto do botão conforme a opção selecionada na
# ComboBox

    def MR_TypeSetter_Refresh(self):
        dic_aux = self._typesetter_config_options[0]
        self.ui.MR_TypeSetter_Button.setText(dic_aux[str(self.ui.MR_TypeSetter_ComboBox.currentIndex())])

    def MC_TypeSetter_Refresh(self):
        dic_aux = self._typesetter_config_options[1]
        self.ui.MC_TypeSetter_Button.setText(dic_aux[str(self.ui.MC_TypeSetter_ComboBox.currentIndex())])

    def Others_TypeSetter_Refresh(self):
        dic_aux = self._typesetter_config_options[2]
        self.ui.Others_TypeSetter_Button.setText(dic_aux[str(self.ui.Others_TypeSetter_ComboBox.currentIndex())])

# As funções abaixo alteram o estado do botão pressionado e garantem que os
# outros sejam desselecionados

    def MR_TypeSetter_Config(self):
        if(not self.ui.MR_TypeSetter_Button.isFlat()):
            self.ui.MR_TypeSetter_Button.setFlat(True)
            self.ui.MC_TypeSetter_Button.setFlat(False)
            self.ui.Others_TypeSetter_Button.setFlat(False)
            self.ui.MR_Control_Button.setFlat(False)
            self.ui.MC_Control_Button.setFlat(False)
            self.ui.Others_Control_Button.setFlat(False)
        else:
            self.ui.MR_TypeSetter_Button.setFlat(False)

    def MC_TypeSetter_Config(self):
        if(not self.ui.MC_TypeSetter_Button.isFlat()):
            self.ui.MR_TypeSetter_Button.setFlat(False)
            self.ui.MC_TypeSetter_Button.setFlat(True)
            self.ui.Others_TypeSetter_Button.setFlat(False)
            self.ui.MR_Control_Button.setFlat(False)
            self.ui.MC_Control_Button.setFlat(False)
            self.ui.Others_Control_Button.setFlat(False)
        else:
            self.ui.MC_TypeSetter_Button.setFlat(False)

    def Others_TypeSetter_Config(self):
        if(not self.ui.Others_TypeSetter_Button.isFlat()):
            self.ui.MR_TypeSetter_Button.setFlat(False)
            self.ui.MC_TypeSetter_Button.setFlat(False)
            self.ui.Others_TypeSetter_Button.setFlat(True)
            self.ui.MR_Control_Button.setFlat(False)
            self.ui.MC_Control_Button.setFlat(False)
            self.ui.Others_Control_Button.setFlat(False)
        else:
            self.ui.Others_TypeSetter_Button.setFlat(False)

    def typesetter_Save_Configs(self):
        # Salva as confgurações do teclado em um arquivo .txt
        config_file = open('configurations/typesetter_config.txt', 'w')
        for i in range(0, len(self._typesetter_config_options)):
            config_file.write(simplejson.dumps(self._typesetter_config_options[i]))
            config_file.flush()
            config_file.write("\n")
            config_file.flush()
        config_file.close()

    def joystick_config(self, increment, option):
        button_index = increment + option
        self._joystick.configure_button(self._joystick.buttons[button_index])
        #print(self._joystick.joystick_config["record"])


    def keyPressEvent(self, event):
        text = ""
        option1 = None
        option2 = None
        key = event.key()

        # Verifica se o botão pressionado é uma das teclas especias abaixo e
        # grava na variavel texto uma string descrevendo a tecla, caso contrio
        # grava o character que representa a tecla

        if(key == Core.Qt.Key_Left):
            text = "Left Arrow"

        elif key == Core.Qt.Key_Right:
            text = "Right Arrow"

        elif key == Core.Qt.Key_Down:
            text = "Down Arrow"

        elif key == Core.Qt.Key_Up:
            text = "Up Arrow"

        elif key == Core.Qt.Key_Space:
            text = "Space"

        elif key == Core.Qt.Key_Control:
            text = "Ctrl"

        elif key == Core.Qt.Key_Alt:
            text = "Alt"

        elif key == Core.Qt.Key_Return:
            text = "Return"

        elif key == Core.Qt.Key_Enter:
            text = "Enter"

        elif key == Core.Qt.Key_Shift:
            text = "Shift"

        elif key == Core.Qt.Key_AltGr:
            text = "AltGr"

        else:
            text = event.text()

        # Verifica qual a opção selecionada
        if(self.ui.MR_TypeSetter_Button.isFlat()):
            option1 = 0
            option2 = self.ui.MR_TypeSetter_ComboBox.currentIndex()

        elif(self.ui.MC_TypeSetter_Button.isFlat()):
            option1 = 1
            option2 = self.ui.MC_TypeSetter_ComboBox.currentIndex()

        elif(self.ui.Others_TypeSetter_Button.isFlat()):
            option1 = 2
            option2 = self.ui.Others_TypeSetter_ComboBox.currentIndex()

        # faz uma copia do dicionario que contem a configuração selcionada,
        # substitui a informação anterior pela tecla pressiona e substituio
        # o dicionario que contém a informação antiga pelo atual

        dic_aux = self._typesetter_config_options[option1]
        dic_aux[str(option2)] = str(text)
        self._typesetter_config_options[option1] = dic_aux

        # Atualiza a iformação mostrada no botões
        self.MR_TypeSetter_Refresh()
        self.MC_TypeSetter_Refresh()
        self.Others_TypeSetter_Refresh()

    def __del__(self):
        self.ui = None
