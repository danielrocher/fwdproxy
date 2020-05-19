#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Written by Daniel Rocher <daniel.rocher@resydev.fr>
# Copyright (C) 2018


import threading, socket, re

class PeerSocket(threading.Thread):
    """This class receive/send packets from/to peer"""
    counter=0
    lock=threading.Lock()
    peer_collection={}

    def __init__(self, peer, proxy, callbackread=None, callbackconnected=None, callbackdisconnected=None, debug_mode=False):
        threading.Thread.__init__(self)
        PeerSocket.lock.acquire()
        PeerSocket.counter+=1
        PeerSocket.lock.release()
        self.connection=None
        self.proxy=proxy
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

    def getCredAndProxyAddressPort(self, proxy):
        import base64
        proxy=proxy.replace('http://', '').replace('https://', '')
        resu=proxy.split('@')
        credential=""
        address='127.0.0.1'
        port=3128
        if len(resu)>1:
            try:
                credential=base64.b64encode(resu[0].encode()).decode()
            except:
                pass
            address_port=resu[1]
        else:
            address_port=resu[0]
        resu=address_port.split(':')
        if len(resu)>1:
            address=resu[0]
            port=resu[1]
        else:
            address=resu[0]
            port=None
        try:
            port=int(port)
        except:
            port=3128 # default for squid
        return credential, address, port

    def run(self):
        self.debug("Create new Thread: {}".format(self.getName()))

        if self.proxy:
            cred, self.host, self.port=self.getCredAndProxyAddressPort(self.proxy)

        self.host_target, self.port_target=self.peer
        PeerSocket.lock.acquire()
        PeerSocket.peer_collection[self.getName()]=self
        PeerSocket.lock.release()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # keepalive
        # after 60 seconds, start sending keepalives every 20 seconds. Stop connection after 3 failed keepalives
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60) # start after n secs.
        self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 20) # interval
        self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3) # count
        try:
            self.connection.connect((self.host, self.port))
        except:
            self.stop()
            return

        if self.proxy:
            self.debug("Use proxy {}:{} (target server is {}:{})".format(self.host, self.port, self.host_target, self.port_target))
            head="CONNECT {0}:{1} HTTP/1.1\r\n" \
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0\r\n" \
            "Proxy-Connection: keep-alive\r\n" \
            "Connection: keep-alive\r\n" \
            "Proxy-Authorization: Basic {2}==\r\n" \
            "Host: {0}:{1}\r\n".format(self.host_target, self.port_target, cred)
            head+="\r\n"
            try:
                self.connection.send(head.encode())
                self.connection.settimeout(5.0)
                r = self.connection.recv(1024)
            except:
                self.debug("TimeOut - Impossible to connect to {} with proxy ({}:{})".format(self.host_target, self.host, self.port))
                self.stop()
                return
            if not re.match(r'HTTP/.{1,3}\s200\s' , r.decode()):
                self.debug("Impossible to connect to {} with proxy ({}:{})".format(self.host_target, self.host, self.port))
                self.stop()
                return
            else:
                self.debug("Proxy - {}".format(r.decode()).strip())

        if self.callbackconnected:
            self.callbackconnected() # forward
        self.eventConnected.set()

        while 1:
            if self.eventTerminated.is_set(): break
            try:
                data= self.connection.recv(2048)
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
        del (PeerSocket.peer_collection[self.getName()])
        PeerSocket.lock.release()
        self.debug ("number of PeerSocket: {}".format(PeerSocket.counter))


if __name__ == "__main__":
    c=PeerSocket(('127.0.0.1', 8080), debug_mode=True)
    c.start()
    c.waitUntilConnected(timeout=5)
    c.sendDatas(b'get index.php')
    c.join()


