#!/usr/bin/env python

import xmlrpclib
import time

server_name = 'http://localhost:8000'
server = xmlrpclib.ServerProxy(server_name)

def main():

    i = 0
   # server.setReady(True)
    while i < 10:
        raw_input("Press Enter to continue...")
        server.setPause(False)
        i = i + 1







if __name__ == '__main__':
    main()