#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json

from datetime import datetime, date, time, timedelta


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc = {}

    def json2registered(self):
        try:
            with open('registered.json', 'r') as outfile_json:
                json.load(self.dicc, outfile_json)
        except:
            self.dicc = {}

    def register2json(self):
        with open('registered.json', 'w') as outfile_json:
            json.dump(self.dicc, outfile_json, indent=3)

    def handle(self):
        line = self.rfile.read()
        doc = line.decode('utf-8').split(" ")
        ip = self.client_address[0]
        port = self.client_address[1]
        if doc[0] == 'REGISTER':
            user = doc[2]
            formato = '%Y-%m-%d %H:%M:%S'
            tiempo = datetime.now()
            expires = doc[4].split('\r\n')[0]
            expired = tiempo + timedelta(seconds=int(expires))
            address = str(ip) + ":" + str(port)
            fecha = expired.strftime(formato)
            self.dicc[user] = {'address': address, 'Expires': fecha}
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            if expires == '0':
                del self.dicc[user]
            lista = []
            for user in self.dicc:
                if self.dicc[user]['Expires'] <= tiempo.strftime(formato):
                    lista.append(user)
            for user in lista:
                del self.dicc[user]
            print(self.dicc)
            print()
            self.register2json()
if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    try:
        PORT = int(sys.argv[1])
    except IndexError:
        sys.exit('Usage: server.py puerto')
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
