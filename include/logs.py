#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Written by Daniel Rocher <daniel.rocher@resydev.fr>
# Copyright (C) 2018


import logging
import logging.handlers
import threading
from datetime import datetime

class Logs(threading.Thread):
    def __init__(self, syslog, logfilename, maxbytes, backupcount, logconnect, logblocked):
        threading.Thread.__init__(self)
        self.logconnect=logconnect
        self.logblocked=logblocked
        self.logger = logging.getLogger('fwproxyd')
        self.logger.setLevel(logging.DEBUG)
        self.lock=threading.Lock()
        # cache
        self.cacheDic={}
        self.cacheTable=[]
        self.lockcache=threading.Lock()
        self.limitsizeoftable=90 # size of cache entries
        self.wait=8

        # if syslog
        if syslog:
            formattersyslog = logging.Formatter('%(name)s: [%(levelname)s] %(message)s')
            try:
                handlersyslog = logging.handlers.SysLogHandler(address = '/dev/log')
                handlersyslog.setFormatter(formattersyslog)
                self.logger.addHandler(handlersyslog)
            except:
                print('Impossible to write to syslog !')
        
        # custom file log
        if logfilename:
            formattercustom = logging.Formatter('%(asctime)s %(name)s: [%(levelname)s] %(message)s')
            try:
                handlerrotate = logging.handlers.RotatingFileHandler(logfilename, maxBytes=maxbytes, backupCount=backupcount)
                handlerrotate.setFormatter(formattercustom)
                self.logger.addHandler(handlerrotate)
            except:
                print('Impossible to write to {} !'.format(logfilename))

    def shouldIprint(self, ipsrc, domain):
        """limit to one entry/self.wait (in seconds)
        return True if it's ok to print"""
        # search in cache
        current=datetime.timestamp(datetime.now())
        decision=True # default

        if (ipsrc, domain) in self.cacheTable:
            try:
                dt=self.cacheDic[(ipsrc, domain)]
                if current > (dt + self.wait):
                    self.lockcache.acquire()
                    self.cacheDic[(ipsrc, domain)]=current
                    self.lockcache.release()
                else:
                    decision=False
            except:
                pass

        else: # not in cache
            # update cache
            self.lockcache.acquire()
            self.cacheTable.append((ipsrc, domain))
            self.cacheDic[(ipsrc, domain)]=current
            # purge cache
            try:
                if len(self.cacheTable)>self.limitsizeoftable:
                    del self.cacheDic[self.cacheTable[0]]
                    del self.cacheTable[0] # remove oldest
            except:
                print ("error : impossible to purge ! ")

            self.lockcache.release()

        return decision

    def logConnect(self, ipsrc, domain):
        if self.logconnect:
            if self.shouldIprint(ipsrc, domain):
                self.lock.acquire()
                try:
                    self.logger.info("CONNECT - src: {} - dst: {}".format(ipsrc, domain))
                except:
                    pass
                self.lock.release()

    def logBlocked(self, ipsrc, domain):
        if self.logblocked:
            if self.shouldIprint(ipsrc, domain):
                self.lock.acquire()
                try:
                    self.logger.warning("BLOCKED - src: {} - dst: {}".format(ipsrc, domain))
                except:
                    pass
                self.lock.release()

    def logServices(self, msg):
        self.lock.acquire()
        try:
            self.logger.info(msg)
        except:
            pass
        self.lock.release()

if __name__ == "__main__":
    filename="test.log"
    log=Logs(False, filename, 10000, 4, True, True)
    log.logConnect('192.168.1.1', 'www.test.fr')
    log.logBlocked('192.168.1.1', 'www.blocked.net')
    log.logServices("Is OK !")
    with open(filename, 'r') as fd:
        print(fd.read())
    import os
    os.remove(filename)


