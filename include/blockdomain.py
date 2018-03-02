#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Written by Daniel Rocher <daniel.rocher@resydev.fr>
# Copyright (C) 2018

import threading, re

class BlockDomain(threading.Thread):
    def __init__(self, filename=None, debug_mode=False):
        self.filename=filename
        self.debug_mode=debug_mode
        if self.filename:
            self.parseFile()

    def debug(self, msg):
        if self.debug_mode:
            print (msg)

    def parseFile(self):
        try:
            with open(self.filename, 'r') as fd:
                for line in fd:
                    line=line.replace('\\','').strip()
                    line=line.replace(' ','') # remove spaces
                    line=re.sub('#.*','', line) # remove comments
                    line=re.sub('http.*://','', line)
                    line=re.sub('/.*','', line) # remove url
                    line=re.sub('^\.*','', line) # remove joker
                    line=re.sub('[$*\^\n]', '', line)
                    if line:
                        BlockDomain.blacklist.append(line)
        except:
            print("Impossible to parse file '{}'".format(self.filename))

    def isDomainAllowed(self, domain):
        for d in BlockDomain.blacklist:
            if domain.endswith(d):
                self.debug("Domain is deny : {}".format(domain))
                return False
        return True


BlockDomain.blacklist=[]

if __name__ == "__main__":
    def testDomain(domain, bd):
        print ("{} : {}".format(domain, bd.isDomainAllowed(domain)))

    bd=BlockDomain("../deny_domain.txt")
    testDomain( "www.test.fr", bd)
    testDomain( "test.fr", bd)
    testDomain( "qwz.fr", bd)
    testDomain( "test.net", bd)
    testDomain( "fr.test.net", bd)