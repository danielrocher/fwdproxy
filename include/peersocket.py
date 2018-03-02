#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Written by Daniel Rocher <daniel.rocher@resydev.fr>
# Copyright (C) 2018


import threading, socket

class PeerSocket(threading.Thread):
    """This class receive/send packets from/to peer"""
    counter=0
    lock=threading.Lock()
    peer_collection={}

    def __init__(self, peer, callbackread=None, callbackconnected=None, callbackdisconnected=None, debug_mode=False):
        threading.Thread.__init__(self)
        PeerSocket.lock.acquire()
        PeerSocket.counter+=1
        PeerSocket.lock.release()
        self.connection=None
        self.peer=peer
        self.eventConnected = threading.Event()
        self.eventTerminated = threading.Event()
        self.lockStoppingSocket=threading.Lock()
        self.debug_mode=debug_mode
        self.callbackread=callbackread
        self.callbackconnected=callbackconnected
        self.callbackdisconnected=callbackdisconnected
            
        self.debug ("number of PeerSocket: {}".format(PeerSocket.counter))

    def debug(self, msg):
        if self.debug_mode:
            print (msg)


    def readyReadHandler(self, data):
        self.debug("PeerSocket.readyReadHandler()")
        if self.callbackread:
            self.callbackread(data)

    def sendDatas(self, data):
        """Send datas to server"""
        if not self.eventConnected.is_set() or self.eventTerminated.is_set(): return
        self.debug("PeerSocket.sendDatas()")
        try:
            self.connection.send(data)
        except socket.error:
             self.debug('socket connection broken')

    def waitUntilConnected(self, timeout=10):
        self.eventConnected.wait(timeout)

    def run(self):
        self.debug("Create new Thread: {}".format(self.getName()))
        PeerSocket.peer_collection[self.getName()]=self
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection.connect(self.peer)
        except:
            self.stop()
            
        self.eventConnected.set()
        if self.callbackconnected:
            self.callbackconnected() # forward

        while 1:
            if self.eventTerminated.is_set(): break
            try:
                data= self.connection.recv(1024)
            except socket.error:
                self.debug('socket connection broken')
                break
            if not data: break
            self.readyReadHandler(data)

        self.stop() # close socket properly


    def stop(self):
        """stop connection with peer"""
        self.lockStoppingSocket.acquire()
        if self.eventTerminated.is_set():
            self.lockStoppingSocket.release()
            return # already stopped
        self.eventTerminated.set()
        self.lockStoppingSocket.release()
        self.debug ("stopping connection with peer {0} - {1}".format(self.peer, self.getName()))
        try:
            self.connection.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.eventConnected.clear()
        if self.callbackdisconnected:
            self.callbackdisconnected() # forward
        self.connection.close()
        PeerSocket.lock.acquire()
        PeerSocket.counter-=1
        PeerSocket.lock.release()
        self.debug ("number of PeerSocket: {}".format(PeerSocket.counter))
        del (PeerSocket.peer_collection[self.getName()])


if __name__ == "__main__":
    c=PeerSocket(('127.0.0.1', 8080), debug_mode=True)
    c.start()
    c.waitUntilConnected(timeout=5)
    c.sendDatas(b'get index.php')
    c.join()


