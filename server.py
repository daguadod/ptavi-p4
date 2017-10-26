#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc = {}
    def handle(self):
        line = self.rfile.read()
        doc = line.decode('utf-8').split(" ")
        ip = self.client_address[0]
        port = self.client_address[1]
        if doc[0] == 'REGISTER':
            user = doc[2]
            address = str(ip) + ":" + str(port)
            self.dicc[user] = ['address: ' + address]
            print (self.dicc)
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
