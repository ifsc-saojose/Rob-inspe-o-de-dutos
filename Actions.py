# -*- coding: utf-8 -*-
import socket
import netifaces as ni
import serial
import sys
import glob

_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_porta_serial = serial.Serial()


def Set_Address(UDP_PORT=5505):
    interfaces = ni.interfaces()

    for i in range(len(interfaces)):
        try:
            UDP_IP = ni.ifaddresses(interfaces[i])[2][0]['addr']
            if(UDP_IP != '127.0.0.1'):
                #_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # UDP
                _sock.bind((UDP_IP, UDP_PORT))
                break

        except:
            print('Interface ' + interfaces[i] + ' is down.')


def Receive_File():
    img = open('img/img.jpg', 'wb')    # Cria um arquivo .jpg

    data, addr = _sock.recvfrom(1024)    # recebe pacote com paylod de 1 K

    # Enquanto nao receber a confirmacao de que a transmissao foi encerrada
    # grava a informacao no arquivo .jpg.

    while (data != 'end'):

        img.write(data)
        img.flush()
        data, addr = _sock.recvfrom(1024)

    # Fecha o arquivo .jpg
    img.close()


def serial_ports():
    """Lists serial ports

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def Serial_Open(porta, baud_rate):
    _porta_serial.port = porta
    _porta_serial.baudrate = baud_rate
    _porta_serial.timeout = 0.1
    _porta_serial.open()


def Serial_Read():
    return _porta_serial.read()
