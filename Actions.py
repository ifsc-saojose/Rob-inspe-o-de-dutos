# -*- coding: utf-8 -*-
import socket
import netifaces as ni
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
