#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Written by Daniel Rocher <daniel.rocher@resydev.fr>
# Copyright (C) 2018

import threading, socket, re
try:
    from include.peersocket import *
    from include.tlshelloparser import *
except:
    from peersocket import *
    from tlshelloparser import *

# Capabilities
class Cap():
    pass

    @staticmethod
    def port(t):
        if t==Cap.http:
            return 80
        else:
            return 443
Cap.http=10
Cap.https=11

class ClientSocket(threading.Thread):
    """This class dialogs with client. (One object/client)"""
    counter=0
    lock=threading.Lock()
    client_collection={}

    def __init__(self, socket, bkdomain, proxy, template_redirect=None, debug_mode=False):
        threading.Thread.__init__(self)
        ClientSocket.lock.acquire()
        ClientSocket.counter+=1
        ClientSocket.lock.release()
        self.type=None # http or https
        self.hostname=None
        self.proxy=proxy
        self.template_redirect=template_redirect
        self.socket=socket
        try:
            self.srcname=socket.getpeername()[0]
        except:
            self.srcname=""
        self.bkdomain=bkdomain
        self.peersock=None
        self.eventPeerconnected = threading.Event()
        self.eventForward = threading.Event()
        self.eventTerminated = threading.Event()
        self.lockStoppingSocket=threading.Lock()
        self.debug_mode=debug_mode
        self.callbacklogconnect=None
        self.callbacklogblocked=None
        self.tlshelloparser=TLSHelloParser(self.debug_mode)
        self.debug ("number of ClientSocket: {}".format(ClientSocket.counter))

    def debug(self, msg):
        if self.debug_mode:
            print (msg)

    def setCallBackLogConnect(self, callbacklogconnect):
        self.callbacklogconnect=callbacklogconnect

    def setCallBackLogBlocked(self, callbacklogblocked):
        self.callbacklogblocked=callbacklogblocked

    def getUrl_Host_fromHTTPheader(self, data):
        self.debug("ClientSocket.getUrl_Host_fromHTTPheader()")
        def decode(data):
            try:
                return data.decode("ascii")
            except:
                pass
            try:
                return data.decode("latin-1")
            except:
                pass
            try:
                return data.decode("utf-8")
            except:
                return ""

        heads = decode(data).strip().split("\n")

        url = None
        hostname = None
        method = None
        if heads:
            for head in heads:
                match = re.match("^(get|post|put|head|delete|connect|trace|options|propfind|merge) ([^ ]+).*$", head.strip(), re.I)
                if (match):
                    method=match.group(1)
                    url = match.group(2)
                match = re.match("^host: ([^ ]+).*$", head.strip(), re.I)
                if (match):
                    hostname = match.group(1)
            if hostname:
                self.debug("Host : {}, {} {}".format(hostname, method, url))
                self.debug(heads)
        return hostname, url

    def connectToPeer(self, p):
        self.debug("ClientSocket.connectToPeer()")
        self.eventForward.set() # forward is now enabled
        self.peersock=PeerSocket(p, self.proxy, callbackread=self.sendDatas, callbackconnected=self.peerConnected, callbackdisconnected=self.peerDisconnected, debug_mode=self.debug_mode)
        self.peersock.start()
        self.peersock.waitUntilConnected(timeout=10)

    def redirect(self):
        self.debug("ClientSocket.redirect()")
        # for http
        if self.type==Cap.http:
            from datetime import datetime
            
            now = datetime.utcnow()
            date_rfc822=now.strftime('%a, %d %b %Y %H:%M:%S GMT')
            tmpl=self.template_redirect.replace('$date$', date_rfc822)
            tmpl=tmpl.replace('$domain$', self.hostname)
            t=tmpl.split("\n\n")
            if len(t)>1:
                heads=t[0]
                content=t[1]
                heads=heads.replace('$length$', str(len(content)))
                # replace LF by CRLF (see RFC 2616)
                heads="\r\n".join([c.replace('\r', '') for c in heads.split('\n')])
                tmpl=heads+"\r\n"*2+content
                # send redirection
                self.sendDatas(tmpl.encode())

    def doForwardIfAllowed(self, data):
        self.debug("ClientSocket.doForwardIfAllowed()")
        # if socket is open, and if it's already allowed, just forward (no need to parse)
        if self.eventForward.is_set() and self.eventPeerconnected.is_set():
            try:
                self.peersock.sendDatas(data)
                return True
            except:
                pass
        return False

    def readyReadHandler(self, data):
        self.debug("ClientSocket.readyReadHandler()")

        # if socket is open, and if it's already allowed, just forward (no need to parse)
        if self.doForwardIfAllowed(data):
            return
        
        # test if is HTTP
        if not self.type:
            self.hostname, url=self.getUrl_Host_fromHTTPheader(data)
            if self.hostname:
                self.type=Cap.http

        # test if is HTTPS
        if not self.type:
            self.tlshelloparser.parseClientHelloHanshake(data)
            self.hostname=self.tlshelloparser.getHostname() # get hostname in client hello handshake
            if self.hostname:
                self.type=Cap.https

        if not self.type:
            self.debug("Impossible to detect protocol !!! -> disconnect")
            self.stop()
            return
        else:
            if not self.bkdomain.isDomainAllowed(self.hostname):
                if self.template_redirect: # if redirect is enabled
                    self.redirect()
                if self.callbacklogblocked:
                    self.callbacklogblocked(self.srcname, self.hostname)
                self.debug("Domain is deny : {} !!! -> disconnect".format(self.hostname))
                self.stop()
                return

            if not self.eventForward.is_set():
                # now, connect and enable forwarding
                self.connectToPeer((self.hostname, Cap.port(self.type)))
                self.doForwardIfAllowed(data)

    def sendDatas(self, data):
        """Send datas to client"""
        if self.eventTerminated.is_set(): return
        self.debug("ClientSocket.sendDatas()")
        try:
            self.socket.send(data)
        except socket.error:
             self.debug('socket connection broken')

    def peerConnected(self):
        self.debug("ClientSocket.peerConnected()")
        if self.callbacklogconnect:
            self.callbacklogconnect(self.srcname, self.hostname)
        self.eventPeerconnected.set()

    def peerDisconnected(self):
        self.debug("ClientSocket.peerDisconnected()")
        self.eventPeerconnected.clear()
        self.stop()

    def run(self):
        self.debug("Create new Thread: {}".format(self.getName()))
        ClientSocket.lock.acquire()
        ClientSocket.client_collection[self.getName()]=self
        ClientSocket.lock.release()
        while 1:
            if self.eventTerminated.is_set(): break
            try:
                data= self.socket.recv(2048)
            except socket.error:
                self.debug('socket connection broken')
                break
            if not data: break
            self.readyReadHandler(data)

        self.stop() # close socket properly


    def stop(self):
        """stop connection with client"""
        self.lockStoppingSocket.acquire()
        if self.eventTerminated.is_set():
            self.lockStoppingSocket.release()
            return # already stopped
        self.eventTerminated.set()
        self.lockStoppingSocket.release()
        self.debug ("stopping connection with client {0} - {1}".format(self.srcname,self.getName()))
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.socket.close()

        # disconnect peer (if connected)
        if self.eventPeerconnected.is_set():
            self.peersock.stop()
            self.peersock.join()
        self.peersock=None
        self.eventPeerconnected.clear()
        self.eventForward.clear()

        ClientSocket.lock.acquire()
        ClientSocket.counter-=1
        del (ClientSocket.client_collection[self.getName()])
        ClientSocket.lock.release()
        self.debug ("number of ClientSocket: {}".format(ClientSocket.counter))


if __name__ == "__main__":
    pass

