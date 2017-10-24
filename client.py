#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

# Constantes. Dirección IP del servidor y contenido a enviar
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
LINEA = sys.argv[3]
LINE = ''
Usuario = sys.argv[4]
LINE = 'REGISTER sip: ' + Usuario + ' SIP/2.0\r\n\r\n'
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    try:
        my_socket.connect((SERVER, PORT))
        print("Enviando:", LINE)
        my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        print('Recibido -- ', data.decode('utf-8'))

    except KeyboardInterrupt:
        print("Finalizado cliente")
