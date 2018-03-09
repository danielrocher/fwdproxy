#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Written by Daniel Rocher <daniel.rocher@resydev.fr>
# Copyright (C) 2018


import logging
import logging.handlers
import threading

class Logs(threading.Thread):
    def __init__(self, syslog, logfilename, maxbytes, backupcount, logconnect, logblocked):
        self.logconnect=logconnect
        self.logblocked=logblocked
        self.logger = logging.getLogger('fwproxyd')
        self.logger.setLevel(logging.DEBUG)
        self.lock=threading.Lock()

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

    def logConnect(self, ipsrc, domain):
        if self.logconnect:
            self.lock.acquire()
            self.logger.info("CONNECT - src: {} - dst: {}".format(ipsrc, domain))
            self.lock.release()

    def logBlocked(self, ipsrc, domain):
        if self.logblocked:
            self.lock.acquire()
            self.logger.warning("BLOCKED - src: {} - dst: {}".format(ipsrc, domain))
            self.lock.release()

    def logServices(self, msg):
        self.lock.acquire()
        self.logger.info(msg)
        self.lock.release()

if __name__ == "__main__":
    filename="test.log"
    log=Logs(False, filename, 10000, 4, True, True)
    log.logConnect('192.168.1.1', 'www.test.fr')
    log.logBlocked('192.168.1.1', 'www.blocked.net')
    log.logServices("Is OK !")
    with open(filename, 'r') as fd:
        print(fd.read())

