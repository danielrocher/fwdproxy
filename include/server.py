#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Written by Daniel Rocher <daniel.rocher@resydev.fr>
# Copyright (C) 2018

import sys, socket
try:
    from include.clientsocket import ClientSocket
    from include.blockdomain import *
except:
    from clientsocket import ClientSocket
    from blockdomain import *

# requirement

if sys.hexversion < 0x030200F0:
        sys.stderr.write ("Python >= 3.2 is required !\n")
        sys.exit(1)


class Server(object):
    def __init__(self, port=8080, filename_bkl=None, debug_mode=False):
        self.port=port
        self.filename_bkl=filename_bkl
        self.started=False
        self.bindsocket=0
        self.debug_mode=debug_mode

    def debug(self, msg):
        if self.debug_mode:
            print (msg)


    def isStarted(self):
        """return True if serveur's running"""
        return self.started


    def createSocketHandler(self, ssl_sock, bkdomain):
        """Reimplement to customize. Return a ClientSocket object"""
        return ClientSocket(ssl_sock, bkdomain, self.debug_mode)


    def start(self):
        """start server"""

        if self.started:
            print ("Server's already started !")
            return # already started


        bkdomain=BlockDomain(self.filename_bkl)

        self.bindsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bindsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.bindsocket.bind(('', self.port))
        except socket.error:
            sys.stderr.write ("Failed to bind to port {}\n".format(self.port))
            sys.exit(1)

        self.bindsocket.listen(1)
        self.debug  ("Server is started.")
        self.started=True

        while 1:
            if self.started==False:
                break
            newsocket, fromaddr = self.bindsocket.accept()
            self.debug ("incomingConnection: {0}, port {1}<->{2}".format(fromaddr[0], fromaddr[1], self.port))

            try:
                client=self.createSocketHandler(newsocket, bkdomain)
                client.start()
            except:
                sys.stderr.write ("Client socket error: {0}, port {1}<->{2}\n".format(fromaddr[0], fromaddr[1], self.port))
                continue


    def stop(self):
        """stop server"""
        if not self.started:
            return # already stopped
        self.started=False

        for key in list(ClientSocket.client_collection):
            try:
                ClientSocket.client_collection[key].stop()
            except:
                pass

        try:
            self.bindsocket.close()
        except:
            pass
        self.bindsocket=0
        self.debug  ("Server is stopped.")


if __name__ == "__main__":
    server=Server(debug_mode=True)
    server.start()
